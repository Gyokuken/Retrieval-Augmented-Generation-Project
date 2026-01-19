import requests
from db import get_conn

OLLAMA_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"


def chunk_text(text, chunk_size=800, overlap=100):
    words = text.split()
    chunks = []

    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start = end - overlap

    return chunks


def embed(text):
    resp = requests.post(
        OLLAMA_URL,
        json={"model": EMBED_MODEL, "prompt": text},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["embedding"]


def ingest_document(text: str, title: str):
    chunks = chunk_text(text)

    conn = get_conn()
    cur = conn.cursor()

    try:
        for idx, chunk in enumerate(chunks):
            embedding = embed(chunk)

            cur.execute(
                """
                INSERT INTO documents
                (content, embedding, source, title, position)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    chunk,
                    embedding,
                    "user_input",
                    title,
                    idx,
                ),
            )

        conn.commit()
        return {
            "status": "ok",
            "chunks_ingested": len(chunks),
        }

    finally:
        cur.close()
        conn.close()
