import tiktoken
from typing import List, Dict

encoding = tiktoken.get_encoding("cl100k_base")

def chunk_text(
    text: str,
    chunk_size: int = 900,
    overlap: int = 150,
    source: str = "user_input",
    title: str = "Untitled"
) -> List[Dict]:

    tokens = encoding.encode(text)
    chunks = []
    start = 0
    chunk_id = 0

    while start < len(tokens):
        end = start + chunk_size
        chunk_tokens = tokens[start:end]

        chunks.append({
            "id": chunk_id,
            "text": encoding.decode(chunk_tokens),
            "metadata": {
                "source": source,
                "title": title,
                "position": chunk_id,
                "start_token": start,
                "end_token": min(end, len(tokens))
            }
        })

        chunk_id += 1
        start += chunk_size - overlap

    return chunks
