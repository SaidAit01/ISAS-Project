import numpy as np
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2') 

def calculate_academic_fit(student_proposals, supervisor_profiles):
    
    # 1. Encode all students at once (This is fine, they are short proposals)
    student_vectors = model.encode(student_proposals)
    
    final_matrix = []
    
    # 2. Loop through each student vector
    # We use enumerate so we can get the vector directly
    for student_vec in student_vectors:
        
        student_scores_against_supervisors = []
        
        # 3. Loop through the RAW text of each supervisor
        for supervisor_text in supervisor_profiles:
            
            # --- THE CHUNKING PROCESS ---
            
            # a. Split the supervisor_text by commas to create a list of chunks
            # Hint: use the .split(',') method
            chunks = supervisor_text.split(',')
            
            # b. Clean the chunks (remove accidental empty spaces)
            # I will give you this line as it's a Python list comprehension trick:
            clean_chunks = [c.strip() for c in chunks if c.strip()]
            
            # c. Now, encode these clean_chunks into vectors!
            chunk_vectors = model.encode(clean_chunks)
            
            # d. Calculate Cosine Similarity between the ONE student_vec 
            # and the MULTIPLE chunk_vectors. 
            scores = util.cos_sim(student_vec, chunk_vectors)[0] # [0] to get the first row, which is our student_vec against all chunks
            
            # e. Find the MAXIMUM score from that comparison
            # Hint: Since 'scores' is a PyTorch tensor, you can use scores.max().item()
            highest_score = scores.max().item()
            
            # f. Append this highest score to our list for this student
            student_scores_against_supervisors.append(highest_score)
            
        # 4. We have finished checking all supervisors for this student. 
        # Append their list of scores to the main matrix.
        final_matrix.append(student_scores_against_supervisors)
        
    # 5. Convert the final python list of lists into a numpy array and return it
    return np.array(final_matrix)