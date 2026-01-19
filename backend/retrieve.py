from db import get_conn
from embeddings import embed_text

def retrieve_chunks(query: str, top_k: int = 6):
    #  Embed query (ensure Python list)
    query_embedding = embed_text(query)
    if hasattr(query_embedding, "tolist"):
        query_embedding = query_embedding.tolist()

    conn = get_conn()
    cur = conn.cursor()

    #  Vector similarity search
    cur.execute(
        """
        SELECT
            content,
            source,
            title,
            position,
            1 - (embedding <-> %s::vector) AS score
        FROM documents
        ORDER BY embedding <-> %s::vector
        LIMIT %s
        """,
        (query_embedding, query_embedding, top_k)
    )

    rows = cur.fetchall()
    conn.close()

    #  Build citation-aware results
    results = []
    for idx, row in enumerate(rows, start=1):
        results.append({
            "id": idx,  # 🔑 citation ID
            "content": row[0],
            "metadata": {
                "source": row[1],
                "title": row[2],
                "position": row[3],
            },
            "score": float(row[4]),
        })

    return results
