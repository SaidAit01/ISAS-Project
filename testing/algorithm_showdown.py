import time
import random
import numpy as np
from scipy.optimize import linear_sum_assignment

def run_rigorous_comparative_benchmark(num_students=200, num_sups=20, cap=10):
    students = list(range(num_students))
    
    # 1. Simulate Realistic Skewed Demand (Market Congestion)
    sup_weights = [5.0, 4.0, 4.0] + [1.0] * (num_sups - 3)
    sup_probs = np.array(sup_weights) / sum(sup_weights)
    
    student_prefs = {}
    for s in students:
        prefs = np.random.choice(range(num_sups), 5, replace=False, p=sup_probs)
        student_prefs[s] = list(prefs)
        
    # 2. Simulate SBERT Scores for GS conflict resolution
    sbert_scores = {
        sup: {s: round(random.uniform(0.3, 0.95), 2) for s in students} 
        for sup in range(num_sups)
    }

    # --- 1. GALE-SHAPLEY (The ISAS Implementation) ---
    def run_gs():
        start = time.time()
        matches = {sup: [] for sup in range(num_sups)} 
        free_students = students.copy()
        current_pref_index = {s: 0 for s in students}

        while free_students:
            s = free_students.pop(0)
            pref_idx = current_pref_index[s]
            
            if pref_idx >= 5:
                continue 
                
            target_sup = student_prefs[s][pref_idx]
            student_score = sbert_scores[target_sup][s]
            
            if len(matches[target_sup]) < cap:
                matches[target_sup].append(s)
            else:
                current_roster = matches[target_sup]
                lowest_student = min(current_roster, key=lambda x: sbert_scores[target_sup][x])
                lowest_score = sbert_scores[target_sup][lowest_student]
                
                if student_score > lowest_score:
                    matches[target_sup].remove(lowest_student)
                    matches[target_sup].append(s)
                    current_pref_index[lowest_student] += 1
                    free_students.append(lowest_student)
                else:
                    current_pref_index[s] += 1
                    free_students.append(s)
        
        exec_time = (time.time() - start) * 1000
        
        # Calculate Welfare: Lower sum is better (Rank 1 is better than Rank 5)
        welfare = 0
        unmatched = 0
        for s in students:
            matched = False
            for idx, sup in enumerate(student_prefs[s]):
                if s in matches[sup]:
                    welfare += (idx + 1)
                    matched = True
                    break
            if not matched:
                welfare += 10 # Penalty score for failing to match
                unmatched += 1
                
        return welfare, exec_time, unmatched

    # --- 2. HUNGARIAN ALGORITHM (Global Optimisation) ---
    def run_ha():
        start = time.time()
        
        # Create slots (cloning 20 supervisors x 10 capacity = 200 slots)
        slots = []
        for sup in range(num_sups):
            slots.extend([sup] * cap)
            
        # Create Cost Matrix: Rows = Students, Cols = Slots
        cost_matrix = np.zeros((num_students, len(slots)))
        
        for i, s in enumerate(students):
            for j, slot_sup in enumerate(slots):
                if slot_sup in student_prefs[s]:
                    cost_matrix[i, j] = student_prefs[s].index(slot_sup) + 1
                else:
                    # Huge penalty if the slot isn't in their top 5
                    cost_matrix[i, j] = 50 
                    
        # Scipy executes the mathematical optimization
        row_ind, col_ind = linear_sum_assignment(cost_matrix)
        exec_time = (time.time() - start) * 1000
        
        welfare = 0
        forced = 0
        for i, s in enumerate(students):
            assigned_slot = col_ind[i]
            assigned_sup = slots[assigned_slot]
            
            if assigned_sup in student_prefs[s]:
                welfare += (student_prefs[s].index(assigned_sup) + 1)
            else:
                welfare += 10 # Penalty for forced allocation outside preferences
                forced += 1
                
        return welfare, exec_time, forced

    # --- EXECUTE AND PRINT ---
    gs_welfare, gs_time, gs_unmatched = run_gs()
    ha_welfare, ha_time, ha_forced = run_ha()

    print(f"{'Algorithm':<20} | {'Welfare (Cost)':<15} | {'Time (ms)':<15} | {'Unmatched/Forced'}")
    print("-" * 75)
    print(f"{'Gale-Shapley (ISAS)':<20} | {gs_welfare:<15} | {gs_time:<10.2f} ms   | {gs_unmatched}")
    print(f"{'Hungarian (Scipy)':<20} | {ha_welfare:<15} | {ha_time:<10.2f} ms   | {ha_forced}")

run_rigorous_comparative_benchmark()