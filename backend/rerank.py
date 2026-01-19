def rerank_chunks(query: str, chunks: list, top_n: int = 3):
    """
    Lightweight reranker using token overlap.
    Keeps original citation IDs intact.
    """

    query_tokens = set(query.lower().split())

    reranked = []
    for chunk in chunks:
        content_tokens = set(chunk["content"].lower().split())
        overlap = len(query_tokens & content_tokens)

        rerank_score = overlap + 0.1 * chunk["score"]

        reranked.append({
            **chunk,
            "rerank_score": rerank_score
        })

    reranked.sort(key=lambda x: x["rerank_score"], reverse=True)

    return reranked[:top_n]
