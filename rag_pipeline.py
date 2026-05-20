"""
RAG Pipeline
  - Document ingestion: PDF / TXT / DOCX
  - Chunking
  - Embeddings: sentence-transformers (free, local)
  - Vector store: ChromaDB (free, local)
  - LLM: Groq API (free tier) with llama-3.3-70b-versatile
"""

import os
import io
import re
import textwrap
from typing import Optional

# ── Third-party imports (installed via requirements.txt) ─────────────────────
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from groq import Groq

# Optional PDF support
try:
    import fitz  # PyMuPDF
    PDF_OK = True
except ImportError:
    PDF_OK = False

# Optional DOCX support
try:
    from docx import Document as DocxDocument
    DOCX_OK = True
except ImportError:
    DOCX_OK = False


CHUNK_SIZE = 600       # characters
CHUNK_OVERLAP = 100
TOP_K = 5             # retrieved chunks per query
COLLECTION_NAME = "banking_docs"

SYSTEM_PROMPT = """You are BankBot, an expert AI banking support assistant.
Use ONLY the provided context to answer customer questions accurately.
If the context does not contain enough information, say so honestly.
Be concise, friendly, and professional.
Always cite relevant policies or terms when applicable."""


class RAGPipeline:
    def __init__(self):
        # Local embeddings (no API key needed)
        print("Loading embedding model...")
        self.embedder = SentenceTransformer("paraphrase-MiniLM-L3-v2")

        # ChromaDB — persisted locally
       
        db_path = os.path.join(os.path.dirname(__file__), ".chromadb")

        self.chroma = chromadb.PersistentClient(path=db_path)

        self.collection = self.chroma.get_or_create_collection(
        name=COLLECTION_NAME
        )

        # Groq client (reads GROQ_API_KEY from env)
        self.groq = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

        print(f"RAG ready. Docs in store: {self.doc_count()}")

    # ── Ingestion ─────────────────────────────────────────────────────────────

    def ingest_bytes(self, data: bytes, filename: str, ext: str) -> int:
        text = self._extract_text(data, ext)
        chunks = self._chunk(text)
        if not chunks:
            return 0
        self._embed_and_store(chunks, source=filename)
        return len(chunks)

    def ingest_file(self, path: str) -> int:
        ext = os.path.splitext(path)[1].lower()
        with open(path, "rb") as f:
            data = f.read()
        return self.ingest_bytes(data, filename=os.path.basename(path), ext=ext)

    def _extract_text(self, data: bytes, ext: str) -> str:
        if ext == ".txt":
            return data.decode("utf-8", errors="ignore")
        if ext == ".pdf":
            if not PDF_OK:
                raise RuntimeError("PyMuPDF not installed. Run: pip install pymupdf")
            doc = fitz.open(stream=data, filetype="pdf")
            return "\n".join(page.get_text() for page in doc)
        if ext == ".docx":
            if not DOCX_OK:
                raise RuntimeError("python-docx not installed. Run: pip install python-docx")
            doc = DocxDocument(io.BytesIO(data))
            return "\n".join(p.text for p in doc.paragraphs)
        raise ValueError(f"Unsupported extension: {ext}")

    def _chunk(self, text: str) -> list[str]:
        text = re.sub(r"\s+", " ", text).strip()
        chunks = []
        start = 0
        while start < len(text):
            end = start + CHUNK_SIZE
            chunks.append(text[start:end])
            start += CHUNK_SIZE - CHUNK_OVERLAP
        return [c for c in chunks if len(c) > 50]

    def _embed_and_store(self, chunks: list[str], source: str):
        embeddings = self.embedder.encode(chunks, show_progress_bar=False).tolist()
        existing = self.collection.count()
        ids = [f"{source}_{existing + i}" for i in range(len(chunks))]
        self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids,
            metadatas=[{"source": source} for _ in chunks],
        )

    # ── Retrieval + Generation ────────────────────────────────────────────────

    def query(self, question: str, history: list[dict]) -> tuple[str, list[str]]:
        # Build retrieval query from last user message + short history
        retrieval_query = self._build_retrieval_query(question, history)

        # Semantic search
        q_embedding = self.embedder.encode([retrieval_query]).tolist()
        results = self.collection.query(
            query_embeddings=q_embedding,
            n_results=min(TOP_K, max(1, self.collection.count())),
        )

        chunks = results["documents"][0] if results["documents"] else []
        sources = list({m["source"] for m in results["metadatas"][0]}) if results["metadatas"] else []

        # Build context
        context = "\n\n---\n\n".join(chunks) if chunks else "No relevant documents found."

        # Build messages for LLM
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "system", "content": f"CONTEXT:\n{context}"},
        ]
        # Add last 6 history turns for conversation memory
        for turn in history[-6:]:
            messages.append(turn)
        messages.append({"role": "user", "content": question})

        # Call Groq
        response = self.groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1024,
            temperature=0.3,
        )
        answer = response.choices[0].message.content.strip()
        return answer, sources

    def _build_retrieval_query(self, question: str, history: list[dict]) -> str:
        """Combine recent history with the new question for better retrieval."""
        recent = " ".join(
            turn["content"] for turn in history[-4:] if turn["role"] == "user"
        )
        return f"{recent} {question}".strip()

    def doc_count(self) -> int:
        return self.collection.count()
