import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL")

def embed_texts(texts: list[str]) -> list[list[float]]:
    embeddings = []

    for text in texts:
        resp = requests.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={
                "model": "nomic-embed-text",
                "prompt": text
            },
            timeout=60
        )
        resp.raise_for_status()
        embeddings.append(resp.json()["embedding"])

    return embeddings


def embed_text(text: str):
    return embed_texts([text])[0]
