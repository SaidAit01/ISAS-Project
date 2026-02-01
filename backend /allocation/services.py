#where the ai logic lives 
import numpy as np
from sentence_transformers import SentenceTransformer, util

# Global variable to load model only once (Efficiency!)
# This prevents reloading the heavy AI model with every single request
model = SentenceTransformer('all-MiniLM-L6-v2') 

def calculate_academic_fit(student_proposals, supervisor_profiles):
    """
    Calculates the cosine similarity between student proposals and supervisor profiles.
    
    Args:
        student_proposals (list of str): List of student topic descriptions.
        supervisor_profiles (list of str): List of supervisor research interests.
    
    Returns:
        numpy.ndarray: A matrix of cosine similarity scores (values between 0 and 1).
    """
    # 1. Encode the inputs into vectors
    # This turns text "I like AI" into numbers [0.1, 0.5, -0.2...]
    student_vectors = model.encode(student_proposals)
    supervisor_vectors = model.encode(supervisor_profiles)
    
    # 2. Calculate Cosine Similarity
    # Result is a matrix of size [Num_Students x Num_Supervisors]
    similarity_matrix = util.cos_sim(student_vectors, supervisor_vectors)
    
    # 3. Return the result as a numpy array for easy processing later
    return similarity_matrix.numpy()