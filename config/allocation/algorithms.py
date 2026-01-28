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