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
student_category = {"Web Application"}

# Supervisor profile also focuses on "Data Analysis" but different tech stack and modality
supervisor_profile = "Researching advanced data analysis using deep learning and neural networks."
supervisor_skills = {"Python", "PyTorch", "Deep Learning"}
supervisor_category = {"Research Simulation"}

# 1. Calculate REAL SBERT Score
student_emb = model.encode(student_abstract)
supervisor_emb = model.encode(supervisor_profile)
real_sbert_score = util.cos_sim(student_emb, supervisor_emb).item()

# 2. Calculate Jaccard Scores for both constraints
jaccard_skills = calculate_jaccard(student_skills, supervisor_skills)
jaccard_category = calculate_jaccard(student_category, supervisor_category)

# 3. Apply Hybrid Weights (Exact system weights: 0.5, 0.3, 0.2)
w1, w2, w3 = 0.5, 0.3, 0.2
final_score = (w1 * real_sbert_score) + (w2 * jaccard_skills) + (w3 * jaccard_category)

print(f"--- Real-World Constraint Accuracy Test ---")
print(f"SBERT Conceptual Score (Weight 0.5): {real_sbert_score:.2f}")
print(f"Jaccard Skills Score (Weight 0.3): {jaccard_skills:.2f}")
print(f"Jaccard Category Score (Weight 0.2): {jaccard_category:.2f}")
print(f"Final Hybrid Score: {final_score:.2f}")

# Calculate the percentage drop from the raw SBERT score to the final penalised score
penalty_percentage = ((real_sbert_score - final_score) / real_sbert_score) * 100
print(f"Penalty applied by discrete constraints: {penalty_percentage:.1f}%")