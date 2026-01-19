import os
import requests

HF_API_KEY = os.getenv("HF_API_KEY")

HF_API_URL = (
    "https://router.huggingface.co/hf-inference/"
    "models/sentence-transformers/all-MiniLM-L6-v2"
)

def embed_text(text: str) -> list[float]:
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json",
    }

    resp = requests.post(
        HF_API_URL,
        headers=headers,
        json={"inputs": text},
        timeout=30,
    )

    if resp.status_code != 200:
        raise RuntimeError(f"HF embedding failed: {resp.status_code} {resp.text}")

    embedding = resp.json()

    # HF returns: [[float, float, ...]]
    return embedding[0]
