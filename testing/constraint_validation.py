from sentence_transformers import SentenceTransformer, util

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

def calculate_jaccard(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union > 0 else 0

# --- THE SCENARIO ---
# Student abstract focuses on "Statistical Data Analysis"
student_abstract = "I am interested in a project involving statistical data analysis and predictive modelling."
student_skills = {"R", "Statistics", "SQL"}

# Supervisor profile also focuses on "Data Analysis" but different tech stack
supervisor_profile = "Researching advanced data analysis using deep learning and neural networks."
supervisor_skills = {"Python", "PyTorch", "Deep Learning"}

# 1. Calculate REAL SBERT Score
student_emb = model.encode(student_abstract)
supervisor_emb = model.encode(supervisor_profile)
real_sbert_score = util.cos_sim(student_emb, supervisor_emb).item()

# 2. Calculate Jaccard Penalty
jaccard_skills = calculate_jaccard(student_skills, supervisor_skills)

# 3. Apply Hybrid Weights (using your actual system weights)
# Assuming w1=0.7 (Semantic) and w2=0.3 (Skills)
w1, w2 = 0.7, 0.3
final_score = (w1 * real_sbert_score) + (w2 * jaccard_skills)

print(f"--- Real-World Constraint Accuracy Test ---")
print(f"SBERT Score (Calculated): {real_sbert_score:.2f}")
print(f"Jaccard Skills Score: {jaccard_skills:.2f}")
print(f"Final Hybrid Score: {final_score:.2f}")
print(f"Penalty applied by Jaccard: {((real_sbert_score - final_score) / real_sbert_score) * 100:.1f}%")