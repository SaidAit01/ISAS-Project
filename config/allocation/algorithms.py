import numpy as np

def generate_hybrid_preferences(student_choices, all_supervisors, ai_scores, n_limit=10):
    """
    Generates preference lists for BOTH students and supervisors.
    """
    # 1. DICTIONARY TO STORE RESULTS
    # We need to return two things: Student prefs and Supervisor prefs
    preferences = {
        'students': [],
        'supervisors': []
    }

    # --- PART A: SUPERVISOR LISTS (Pure AI) ---
    # We loop through the matrix columns. 
    # Supervisor 0 is column 0, Supervisor 1 is column 1...
    num_supervisors = len(all_supervisors)
    num_students = len(ai_scores) # Number of rows
    all_student_indices = list(range(num_students))

    for j in range(num_supervisors):
        # 1. Get the column of scores for this supervisor 'j'
        # Hint: slicing in numpy is [row, column] -> [:, j]
        supervisor_scores = ai_scores[:, j] 
        
        # 2. Sort the students based on these scores (Highest score first!)
        # np.argsort gives indices of sorted elements. [::-1] reverses it for descending order.
        sorted_indices = np.argsort(supervisor_scores)[::-1]
        
        # 3. Add this list of student INDICES to our dictionary
        preferences['supervisors'].append(sorted_indices.tolist())

    # --- PART B: STUDENT LISTS (Hybrid) ---
    for i, choices in enumerate(student_choices):
        # 1. Get AI scores for this student 'i' (Row i)
        scores = ai_scores[i]
        
        # 2. Get top N AI recommendations (Indices)
        top_n_indices = np.argsort(scores)[-n_limit:][::-1]
        
        # 3. Convert those indices into Supervisor Names
        ai_suggestions = [all_supervisors[idx] for idx in top_n_indices]
        
        # 4. Combine: Manual Choices + AI Suggestions (Avoiding duplicates)
        # Note: 'choices' is already a list of names like ['Dr. Smith', 'Prof. Jones']
        final_list = list(choices)
        for supervisor in ai_suggestions:
            if supervisor not in final_list:
                final_list.append(supervisor)
        
        preferences['students'].append(final_list)

    return preferences

def spa_allocation(student_prefs, supervisor_prefs, capacities, supervisor_names):
    """
    Executes the Student-Project Allocation (SPA) algorithm.
    
    Args:
        student_prefs (dict): {student_index: ['Dr. A', 'Dr. B'...]}
        supervisor_prefs (dict): {supervisor_index: [student_id_1, student_id_2...]}
        capacities (dict): {supervisor_name: capacity_int}
        supervisor_names (list): List of supervisor names to map names -> IDs.
        
    Returns:
        dict: Final matches {supervisor_name: [student_index, ...]}
    """
    # 1. SETUP
    # Create a mapping from "Dr. Smith" -> ID 0
    sup_name_to_id = {name: i for i, name in enumerate(supervisor_names)}
    
    # Track matches: {supervisor_id: [student_id, ...]}
    matches = {i: [] for i in range(len(supervisor_names))}
    
    # Track which student is unmatched. Initially ALL are unmatched.
    # We use a Queue (list) for efficiency.
    unmatched_students = list(student_prefs.keys())
    
    # Track where each student is in their preference list (0 = 1st choice, 1 = 2nd...)
    student_next_proposal_index = {s_id: 0 for s_id in unmatched_students}

    # 2. THE MAIN LOOP (Gale-Shapley)
    while unmatched_students:
        # a. Pick an unmatched student
        student_id = unmatched_students[0]
        
        # Get their preference list
        my_prefs = student_prefs[student_id]
        
        # Check if they have run out of choices (Project Failure case)
        if student_next_proposal_index[student_id] >= len(my_prefs):
            unmatched_students.pop(0) # Remove them, they are unassigned
            continue

        # b. Get the supervisor they want to propose to
        sup_name_choice = my_prefs[student_next_proposal_index[student_id]]
        sup_id = sup_name_to_id.get(sup_name_choice)
        
        # Increment their progress for next time
        student_next_proposal_index[student_id] += 1
        
        if sup_id is None: continue # Skip invalid names

        # c. Check Supervisor Capacity
        current_matches = matches[sup_id]
        capacity = capacities.get(sup_name_choice, 5) # Default capacity 5 if missing
        
        # CASE 1: Supervisor has space
        if len(current_matches) < capacity:
            matches[sup_id].append(student_id)
            unmatched_students.pop(0) # Student is now matched!
            
        # CASE 2: Supervisor is FULL - Challenge Step
        else:
            # We must find the "worst" student currently matched to this supervisor
            # We look at the Supervisor's Preference List to judge.
            sup_ranking_list = supervisor_prefs[sup_id] # List of student IDs sorted best to worst
            
            # Find the rank of the NEW student
            # (If student not in list, rank is Infinity/Bad)
            try:
                new_student_rank = sup_ranking_list.index(student_id)
            except ValueError:
                new_student_rank = float('inf')

            # Find the rank of the WORST current student
            worst_student_id = -1
            worst_rank = -1
            
            for matched_student in current_matches:
                try:
                    rank = sup_ranking_list.index(matched_student)
                except ValueError:
                    rank = float('inf')
                
                if rank > worst_rank: # Higher index = Worse rank
                    worst_rank = rank
                    worst_student_id = matched_student
            
            # d. The Stability Check
            # If the new student is BETTER (lower rank index) than the worst current one:
            if new_student_rank < worst_rank:
                # KICK OUT the worst student
                matches[sup_id].remove(worst_student_id)
                unmatched_students.append(worst_student_id) # They go back to the queue
                
                # ACCEPT the new student
                matches[sup_id].append(student_id)
                unmatched_students.pop(0) # Remove new student from queue
            else:
                # REJECTION: Supervisor keeps current students. 
                # Student S stays in queue and will try next choice in next loop.
                pass

    # 3. FORMAT OUTPUT (Convert IDs back to Names for display)
    final_allocation = {}
    for sup_id, student_ids in matches.items():
        sup_name = supervisor_names[sup_id]
        final_allocation[sup_name] = student_ids
        
    return final_allocation