from sentence_transformers import SentenceTransformer, CrossEncoder, util
from sklearn.feature_extraction.text import TfidfVectorizer
import torch
import torch.nn.functional as F

# Test inputs
student_text = "Deep Neural Networks"
supervisor_text = "Machine Learning and Artificial Intelligence"

print("--- Running Algorithmic Comparison ---")

# 1. TF-IDF Calculation (Lexical)
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform([student_text, supervisor_text])
tfidf_sim = (tfidf_matrix * tfidf_matrix.T).toarray()[0, 1]
print(f"TF-IDF Similarity: {tfidf_sim:.2f}")

# 2. SBERT Calculation (Bi-Encoder / ISAS Choice)
bi_model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = bi_model.encode([student_text, supervisor_text])
sbert_sim = util.cos_sim(embeddings[0], embeddings[1]).item()
print(f"SBERT Bi-Encoder Similarity: {sbert_sim:.2f}")

# 3. Standard BERT (Cross-Encoder)
# This line was likely missing in your last run:
cross_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

# Use double brackets for the pair
cross_sim_logit = cross_model.predict([[student_text, supervisor_text]])

# Convert logit to a 0-1 probability
probability = torch.sigmoid(torch.tensor(cross_sim_logit[0])).item()

print(f"Standard BERT Cross-Encoder Score (Logit): {cross_sim_logit[0]:.2f}")
print(f"Standard BERT Cross-Encoder Score (Probability): {probability:.2f}")