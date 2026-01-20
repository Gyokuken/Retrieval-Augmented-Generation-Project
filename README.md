# Simple RAG System (FastAPI + Groq)

A minimal, production-ready **Retrieval-Augmented Generation (RAG)** backend built with **FastAPI**, **LangChain**, and **Groq LLMs**.  
You ingest documents, embed them, store them in a vector database, and query them using an LLM that actually knows your data instead of hallucinating nonsense.

---

## Features

- FastAPI backend
- Groq-powered LLM inference (fast + cheap)
- Document ingestion & chunking
- Vector search using embeddings
- Clean RAG pipeline (Retriever → LLM → Answer)
- Easy to extend (frontend, auth, DB swap, etc.)

---

## Architecture (High Level)

1. Documents are loaded and split into chunks  
2. Chunks are converted to embeddings  
3. Embeddings are stored in a vector store  
4. User query → relevant chunks retrieved  
5. Groq LLM generates an answer using retrieved context  

This is **actual RAG**, not “prompt stuffing pretending to be RAG”.

---

## Project Structure

```sh
├── backend/
│ ├── main.py # FastAPI entry point
│ ├── rag.py # RAG pipeline logic
│ ├── ingest.py # Document ingestion
│ ├── seed.py # Initial data seeding
│ ├── config.py # Environment & constants
│ └── requirements.txt
├── data/ # Documents to ingest
└── README.md
```


---

## Requirements

- Python **3.9+**
- Groq API key
- Virtual environment (recommended unless you enjoy dependency hell)

---

## Installation

```bash
git clone <your-repo-url>
cd backend

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```
---

## Environment Variables
Create a .env file inside backend/:
```bash
GROQ_API_KEY=your_groq_api_key_here
```
No key = no LLM = system is useless. Don’t skip this.

Seeding / Ingesting Data
Put your documents inside the data/ folder, then run:
```bash
python seed.py
```
---

This will:

-- Load documents

-- Split them into chunks

-- Generate embeddings

-- Store them in the vector database

-- Run this once, or whenever data changes.

Running the Server
``` bash
uvicorn main:app --reload
```

Server will start at:
```bash
http://127.0.0.1:8000
```

---

Swagger UI (use this, it's there for a reasons)
```bash
http://127.0.0.1:8000/docs
```
## Querying the RAG System

Typical flow:

Send a query to the /query endpoint

Backend retrieves relevant chunks

Groq LLM answers using retrieved context only

If your answers are bad:
 
Your chunks are bad

Your embeddings are bad

Or your documents are trash
(Yes, this happens more often than people admit.)

## requirements.txt (Important)
Groq is included — this was missing earlier and that was a legit catch.

```bash
fastapi
uvicorn
python-dotenv
langchain
langchain-community
langchain-groq
chromadb
tiktoken
pydantic
```

If Groq isn’t here, RAG isn’t happening. Period.

---

## Notes & Gotchas
RAG quality depends more on chunking strategy than the LLM

Smaller chunks ≠ always better

Don’t blindly increase k in retrieval — you’ll just add noise

This backend works fine without a frontend; test via Swagger or Postman

---

## Next Obvious Improvements
Auth (JWT)

Streaming responses

Hybrid search (BM25 + vectors)

Persistent vector DB (Postgres + pgvector)

Frontend (only after backend is rock solid)

---

## Final Reality Check

This is a real RAG backend, not a tutorial toy.
If you want hallucination-free answers, this is the baseline — not the finish line.

If you want:

--Advanced chunking

-- Evaluation metrics

-- Multi-document reasoning

-- Agentic RAG

Say the word.
