import os
from groq import Groq
from prompts import SYSTEM_PROMPT

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_answer(query: str, chunks: list):
    if not chunks:
        return {
            "answer": "I could not find relevant information in the provided documents.",
            "sources": []
        }

    # Build grounded context with stable citation IDs
    context_blocks = []
    for i, c in enumerate(chunks, start=1):
        # ensure citation_id exists
        citation_id = c.get("citation_id", i)
        c["citation_id"] = citation_id

        context_blocks.append(
            f"[{citation_id}] {c['content']}"
        )

    context = "\n".join(context_blocks)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": (
                "You are given retrieved document excerpts.\n\n"
                f"Context:\n{context}\n\n"
                f"Question:\n{query}\n\n"
                "Answer ONLY using the context above.\n"
                "If the answer is not present, say you do not know.\n"
                "Cite sources inline using [number]."
            )
        }
    ]

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.2,
    )

    answer_text = completion.choices[0].message.content.strip()

    return {
        "answer": answer_text,
        "sources": [
            {
                "citation": c["citation_id"],
                "content": c["content"],
                "metadata": c["metadata"]
            }
            for c in chunks
        ]
    }
