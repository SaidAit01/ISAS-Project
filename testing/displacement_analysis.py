import time
import random
import numpy as np

def run_rigorous_allocation(num_students=200, num_supervisors=20, cap=10):
    students = list(range(num_students))
    
    # 1. Simulate Skewed Demand (Some supervisors are way more popular)
    # Give supervisors probabilities of being chosen (e.g., first 3 are super popular)
    sup_weights = [5.0, 4.0, 4.0] + [1.0] * (num_supervisors - 3)
    sup_probs = np.array(sup_weights) / sum(sup_weights)
    
    student_prefs = {}
    for s in students:
        # Weighted random choice without replacement
        prefs = np.random.choice(range(num_supervisors), 5, replace=False, p=sup_probs)
        student_prefs[s] = list(prefs)
        
    # 2. Simulate SBERT Scores for tentative Gale-Shapley matching
    # Dictionary of {supervisor: {student: score}}
    simulated_sbert_scores = {
        sup: {s: round(random.uniform(0.3, 0.95), 2) for s in students} 
        for sup in range(num_supervisors)
    }
    
    # {supervisor: [list of matched students]}
    matches = {sup: [] for sup in range(num_supervisors)} 
    displacement = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 'Unmatched': 0}
    
    free_students = students.copy()
    current_pref_index = {s: 0 for s in students}

    # True Gale-Shapley Logic
    while free_students:
        s = free_students.pop(0)
        pref_idx = current_pref_index[s]
        
        if pref_idx >= 5:
            continue # Student exhausted all preferences
            
        target_sup = student_prefs[s][pref_idx]
        student_score = simulated_sbert_scores[target_sup][s]
        
        # If supervisor has space, tentative accept
        if len(matches[target_sup]) < cap:
            matches[target_sup].append(s)
        else:
            # Supervisor is full. Do they prefer this new student?
            # Find the current matched student with the lowest SBERT score
            current_roster = matches[target_sup]
            lowest_student = min(current_roster, key=lambda x: simulated_sbert_scores[target_sup][x])
            lowest_score = simulated_sbert_scores[target_sup][lowest_student]
            
            if student_score > lowest_score:
                # Kick out the lowest scoring student (Displacement!)
                matches[target_sup].remove(lowest_student)
                matches[target_sup].append(s)
                # Put rejected student back in queue for their next preference
                current_pref_index[lowest_student] += 1
                free_students.append(lowest_student)
            else:
                # Student is rejected
                current_pref_index[s] += 1
                free_students.append(s)

    # Calculate final displacement accurately based on final matches
    for s in students:
        matched = False
        for pref_idx, sup in enumerate(student_prefs[s]):
            if s in matches[sup]:
                displacement[pref_idx + 1] += 1
                matched = True
                break
        if not matched:
            displacement['Unmatched'] += 1

    print("--- True Gale-Shapley Displacement Results ---")
    for choice, count in displacement.items():
        print(f"Choice {choice}: {count} students ({(count/num_students)*100:.1f}%)")

run_rigorous_allocation()