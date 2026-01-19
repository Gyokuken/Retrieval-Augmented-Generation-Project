from fastapi import FastAPI
from pydantic import BaseModel
from ingest import ingest_document
from retrieve import retrieve_chunks
from rerank import rerank_chunks
from answer import generate_answer
from fastapi.middleware.cors import CORSMiddleware
import time



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class IngestRequest(BaseModel):
    text: str
    title: str | None = None

class QueryRequest(BaseModel):
    query: str

@app.post("/ingest")
def ingest(req: IngestRequest):
    return ingest_document(
        text=req.text,
        title=req.title or "User Input"
    )

@app.post("/query")
def query(req: QueryRequest):
    start = time.time()

    retrieved = retrieve_chunks(req.query)
    reranked = rerank_chunks(req.query, retrieved)
    result = generate_answer(req.query, reranked)

    end = time.time()

    # Attach latency info
    result["latency_ms"] = int((end - start) * 1000)

    return result
