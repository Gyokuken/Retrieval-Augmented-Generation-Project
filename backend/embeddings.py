from sentence_transformers import SentenceTransformer
import numpy as np

# Load once at startup (IMPORTANT)
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str) -> list[float]:
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()
