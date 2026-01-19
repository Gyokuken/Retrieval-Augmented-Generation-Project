from db import get_conn
from embeddings import embed_text

def retrieve_chunks(query: str, top_k: int = 6):
    query_embedding = embed_text(query)

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT content, source, title, position,
               1 - (embedding <-> %s::vector) AS score
        FROM documents
        ORDER BY embedding <-> %s::vector
        LIMIT %s
        """,
        (query_embedding, query_embedding, top_k),
    )

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "content": r[0],
            "metadata": {
                "source": r[1],
                "title": r[2],
                "position": r[3],
            },
            "score": float(r[4]),
        }
        for r in rows
    ]
