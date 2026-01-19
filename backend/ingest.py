from db import get_conn
from embeddings import embed_text

def chunk_text(text, chunk_size=800, overlap=100):
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunks.append(" ".join(words[start:end]))
        start = end - overlap

    return chunks


def ingest_document(text: str, title: str):
    chunks = chunk_text(text)

    conn = get_conn()
    cur = conn.cursor()

    for idx, chunk in enumerate(chunks):
        try:
            embedding = embed_text(chunk)
        except Exception :
            return {"error": "Embedding service unavailable"}
            
        cur.execute(
            """
            INSERT INTO documents (content, embedding, source, title, position)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (chunk, embedding, "user_input", title, idx),
        )

    conn.commit()
    cur.close()
    conn.close()

    return {
        "status": "ok",
        "chunks_ingested": len(chunks),
    }

