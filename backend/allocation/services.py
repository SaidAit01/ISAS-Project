import numpy as np
from sentence_transformers import SentenceTransformer, util

# Load the SBERT model once when the server starts
model = SentenceTransformer('all-MiniLM-L6-v2') 

def calculate_hybrid_score(student, supervisor, sbert_score):

    student_skills = set(student.programming_languages)
    required_skills = set(supervisor.required_skills)
    
    if len(required_skills) == 0:
        skill_score = 1.0
    else:
        skill_matches = student_skills.intersection(required_skills)
        skill_score = len(skill_matches) / len(required_skills)
        
    student_categories = set(student.project_category)
    # CRITICAL FIX: Updated to match the new models.py column name!
    suggested_categories = set(supervisor.project_categories)
    
    if len(suggested_categories) == 0:
        category_score = 1.0
    else:
        category_matches = student_categories.intersection(suggested_categories)
        category_score = len(category_matches) / len(suggested_categories)
        
    final_hybrid_score = (sbert_score * 0.5) + (skill_score * 0.3) + (category_score * 0.2)
    return final_hybrid_score


def calculate_academic_fit(students, supervisors):
    """
    Takes the RAW lists of Django Student and Supervisor objects.
    Returns a numpy matrix of the final hybrid scores.
    """
    final_matrix = []
    
    # 1. Loop through every student
    for student in students:
        student_scores = []
        
        # Encode the student's topic description ONCE
        student_vector = model.encode(student.topic_description)
        
        # 2. Loop through every supervisor for this student
        for supervisor in supervisors:
            
            # --- SBERT PHASE ---
            chunk_vectors = model.encode(supervisor.research_interests)
            sbert_tensor = util.cos_sim(student_vector, chunk_vectors)
            sbert_score = sbert_tensor.max().item()
            
            # --- HYBRID PHASE ---
            final_score = calculate_hybrid_score(student, supervisor, sbert_score)
            
            # --- APPEND PHASE ---
            student_scores.append(final_score)
            
        # 3. Append the student's completed row to the final matrix
        final_matrix.append(student_scores)
        
    return np.array(final_matrix)
    