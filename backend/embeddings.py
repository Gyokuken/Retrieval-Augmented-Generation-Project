import os
import requests

HF_API_KEY = os.getenv("HF_API_KEY")

HF_EMBEDDING_URL = (
    "https://router.huggingface.co/hf-inference/models/"
    "sentence-transformers/all-MiniLM-L6-v2"
)

HEADERS = {
    "Authorization": f"Bearer {HF_API_KEY}",
    "Content-Type": "application/json",
}

def embed_text(text: str):
    resp = requests.post(
        HF_EMBEDDING_URL,
        headers=HEADERS,
        json={"inputs": text},
        timeout=30,
    )

    if resp.status_code != 200:
        raise RuntimeError(
            f"HF embedding failed: {resp.status_code} {resp.text}"
        )

    data = resp.json()

    # HF returns: [[float, float, ...]]
    if not isinstance(data, list) or not isinstance(data[0], list):
        raise RuntimeError(f"Unexpected HF response: {data}")

    return data[0]
