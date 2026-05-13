import time
import random
import numpy as np

def rigorous_scalability_benchmark():
    sizes = [10, 50, 100, 200, 300, 400]
    times = []

    print(f"{'Cohort Size (N)':<15} | {'Supervisors':<15} | {'Execution Time (ms)'}")
    print("-" * 55)

    for n in sizes:
        num_sups = max(1, n // 10) 
        cap = 10
        students = list(range(n))
        
        # FIXED: Dynamically build weights so they always match num_sups length
        base_weights = [5.0, 4.0, 4.0]
        if num_sups <= len(base_weights):
            sup_weights = base_weights[:num_sups]
        else:
            sup_weights = base_weights + [1.0] * (num_sups - len(base_weights))
            
        sup_probs = np.array(sup_weights) / sum(sup_weights)
        
        student_prefs = {}
        for s in students:
            num_choices = min(5, num_sups) 
            prefs = np.random.choice(range(num_sups), num_choices, replace=False, p=sup_probs)
            student_prefs[s] = list(prefs)
            
        sbert_scores = {
            sup: {s: round(random.uniform(0.3, 0.95), 2) for s in students} 
            for sup in range(num_sups)
        }
        
        start = time.time()
        
        matches = {sup: [] for sup in range(num_sups)} 
        free_students = students.copy()
        current_pref_index = {s: 0 for s in students}

        while free_students:
            s = free_students.pop(0)
            pref_idx = current_pref_index[s]
            
            if pref_idx >= len(student_prefs[s]):
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
        times.append(exec_time)
        print(f"{n:<15} | {num_sups:<15} | {exec_time:.4f} ms")

    return sizes, times

rigorous_scalability_benchmark()