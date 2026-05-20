"""
Banking Support Chatbot - FastAPI Backend
RAG Pipeline with ChromaDB + Groq (free LLM API)
"""

import os
import uuid
import time
from typing import Optional
from dotenv import load_dotenv

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from rag_pipeline import RAGPipeline

# ─────────────────────────────────────────────────────────────────────────────
# FastAPI App
# ─────────────────────────────────────────────────────────────────────────────
load_dotenv()
app = FastAPI(
    title="Banking Support Chatbot API",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────────────────────────────────────
# Memory Store
# ─────────────────────────────────────────────────────────────────────────────

# Session memory:
# {
#   session_id: [
#       {"role": "user", "content": "..."},
#       {"role": "assistant", "content": "..."}
#   ]
# }

sessions: dict[str, list] = {}

# Initialize RAG pipeline
rag = RAGPipeline()

# ─────────────────────────────────────────────────────────────────────────────
# Request / Response Models
# ─────────────────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    answer: str
    session_id: str
    sources: list[str]


# ─────────────────────────────────────────────────────────────────────────────
# Health Endpoint
# ─────────────────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {
        "status": "ok",
        "timestamp": time.time(),
        "docs_indexed": rag.doc_count()
    }


# ─────────────────────────────────────────────────────────────────────────────
# Upload Endpoint
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    allowed = {".pdf", ".txt", ".docx"}

    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}"
        )

    content = await file.read()

    chunks = rag.ingest_bytes(
        content,
        filename=file.filename,
        ext=ext
    )

    return {
        "message": f"Ingested '{file.filename}' successfully",
        "chunks_added": chunks
    }


# ─────────────────────────────────────────────────────────────────────────────
# Chat Endpoint
# ─────────────────────────────────────────────────────────────────────────────

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):

    # Create session if not provided
    session_id = req.session_id or str(uuid.uuid4())

    # Get session history
    history = sessions.setdefault(session_id, [])

    # Query RAG pipeline
    answer, sources = rag.query(
        req.message,
        history
    )

    # Store conversation
    history.append({
        "role": "user",
        "content": req.message
    })

    history.append({
        "role": "assistant",
        "content": answer
    })

    # Keep last 10 conversation turns
    sessions[session_id] = history[-20:]

    return ChatResponse(
        answer=answer,
        session_id=session_id,
        sources=sources
    )


# ─────────────────────────────────────────────────────────────────────────────
# Clear Session Endpoint
# ─────────────────────────────────────────────────────────────────────────────

@app.delete("/session/{session_id}")
def clear_session(session_id: str):

    sessions.pop(session_id, None)

    return {
        "message": "Session cleared successfully"
    }


# ─────────────────────────────────────────────────────────────────────────────
# Run Server
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )