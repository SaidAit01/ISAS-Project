# testing/sparsity_test.py
from sentence_transformers import SentenceTransformer, util

# Load your ISAS choice model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Scenario: A student with a minimal abstract vs. an enriched profile
supervisor_profile = "Expert in Deep Learning and Neural Networks using PyTorch and Python."

# 1. Baseline: Only the short abstract
abstract_only = "I want to do a project about machine learning."

# 2. Enriched: Abstract + Technical Skills + Project Category 
enriched_input = (
    "Abstract: I want to do a project about machine learning. "
    "Technical Skills: Python, PyTorch, Scikit-learn. "
    "Category: Artificial Intelligence."
)

# Calculate Cosine Similarities
score_low = util.cos_sim(model.encode(abstract_only), model.encode(supervisor_profile)).item()
score_high = util.cos_sim(model.encode(enriched_input), model.encode(supervisor_profile)).item()

print(f"--- Sparsity Failsafe Validation ---")
print(f"Baseline Score (Abstract Only): {score_low:.2f}")
print(f"Enriched Score (Failsafe Active): {score_high:.2f}")

improvement = ((score_high - score_low) / score_low) * 100
print(f"Improvement in Match Confidence: {improvement:.1f}%")