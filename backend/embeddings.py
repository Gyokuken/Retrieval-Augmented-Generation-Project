import os
import requests

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# HF_URL = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{HF_MODEL}"
HF_URL = f"https://router.huggingface.co/hf-inference/pipeline/feature-extraction/{HF_MODEL}"

HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json",
}

def embed_text(text: str) -> list[float]:
    resp = requests.post(
        HF_URL,
        headers=HEADERS,
        json={"inputs": text},
        timeout=30,
    )

    if resp.status_code != 200:
        raise RuntimeError(f"HF embedding failed: {resp.text}")

    embedding = resp.json()

    # HF returns [[...]] for single input
    if isinstance(embedding[0], list):
        embedding = embedding[0]

    return embedding

