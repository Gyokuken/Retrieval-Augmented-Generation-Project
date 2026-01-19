import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

EMBEDDING_MODEL = "nomic-embed-text"  # or recommended Groq embedding model

def embed_texts(texts: list[str]) -> list[list[float]]:
    resp = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )
    return [d.embedding for d in resp.data]

def embed_text(text: str) -> list[float]:
    return embed_texts([text])[0]
