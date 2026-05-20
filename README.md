# 🏦 BankBot — AI Banking Support Chatbot

A full-stack **Retrieval-Augmented Generation (RAG)** banking chatbot built with FastAPI, ChromaDB, Sentence-Transformers, and Groq LLM.

---

## Architecture

```
User Browser (HTML/JS)
       │
       ▼
FastAPI Backend (main.py)
  ├── POST /chat      ← conversation with memory
  ├── POST /upload    ← ingest PDF/TXT/DOCX
  └── GET  /health
       │
       ▼
RAG Pipeline (rag_pipeline.py)
  ├── Text extraction (PyMuPDF / python-docx)
  ├── Chunking (600 chars, 100 overlap)
  ├── Embeddings → all-MiniLM-L6-v2 (local, free)
  ├── Vector Store → ChromaDB (local, persistent)
  └── LLM → Groq API (llama-3.3-70b-versatile, free tier)
```

---

## Prerequisites

- Python 3.10+
- A **free** [Groq API key](https://console.groq.com/keys)
- VS Code (recommended)

---

## Setup in VS Code — Step by Step

### Step 1 — Clone / open the project

Open the `banking-chatbot` folder in VS Code.

### Step 2 — Create a virtual environment (recommended)

```bash
# In the VS Code terminal (Ctrl+`)
python -m venv venv

# Activate it:
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r backend/requirements.txt
```

### Step 4 — Set your Groq API key

```bash
# Copy the example env file
cp backend/.env.example backend/.env
```

Edit `backend/.env` and paste your Groq API key:
```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```

Get a free key at → https://console.groq.com/keys (no credit card required)

### Step 5 — Seed the banking knowledge base

```bash
python scripts/seed_data.py
```

This loads 4 synthetic banking documents into ChromaDB:
- Personal Loan Policy
- Credit Card Terms & Conditions
- Banking FAQs
- RBI Guidelines & Compliance

### Step 6 — Start the backend server

```bash
cd backend
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     RAG ready. Docs in store: 120
```

### Step 7 — Open the frontend

**Option A** — Simple (open directly in browser):
```
Open frontend/index.html in your browser
```

**Option B** — Serve via Python:
```bash
python -m http.server 3000 --directory frontend
# Then visit http://localhost:3000
```

---

## VS Code Tasks (shortcut)

Use `Ctrl+Shift+P` → `Tasks: Run Task`:
1. **Install Dependencies** — `pip install -r backend/requirements.txt`
2. **Seed Data** — loads banking documents into ChromaDB
3. **Start Backend** — runs FastAPI on port 8000
4. **Open Frontend** — serves UI on port 3000

---

## API Reference

### `GET /health`
Returns server status and document count.

### `POST /upload`
Upload a banking document (PDF, TXT, DOCX).
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@my_loan_policy.pdf"
```

### `POST /chat`
Send a message and receive a RAG-powered response.
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the interest rate on personal loans?", "session_id": null}'
```

Response:
```json
{
  "answer": "Personal loan interest rates range from 10.5% to 18% per annum...",
  "session_id": "abc-123",
  "sources": ["personal_loan_policy.txt"]
}
```

### `DELETE /session/{session_id}`
Clears conversation history for a session.

---

## Project Structure

```
banking-chatbot/
├── backend/
│   ├── main.py            ← FastAPI app, routes, session management
│   ├── rag_pipeline.py    ← RAG logic (embed, store, retrieve, generate)
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── index.html         ← Full chatbot UI (vanilla JS, no build step)
├── scripts/
│   └── seed_data.py       ← Seeds synthetic banking data into ChromaDB
├── .vscode/
│   ├── launch.json        ← Debug config
│   └── tasks.json         ← Run tasks
├── render.yaml            ← Cloud deployment config (Render free tier)
└── README.md
```

---

## Cloud Deployment (Render — Free Tier)

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Set environment variable `GROQ_API_KEY` in the Render dashboard
5. Deploy!

The `render.yaml` config handles everything automatically.

---

## Features

- ✅ RAG pipeline (chunk → embed → store → retrieve → generate)
- ✅ ChromaDB vector store (persistent, local)
- ✅ Free local embeddings (all-MiniLM-L6-v2)
- ✅ Free LLM via Groq API (llama-3.3-70b)
- ✅ Session-based conversation memory (last 10 turns)
- ✅ PDF, TXT, DOCX document ingestion
- ✅ Source attribution in responses
- ✅ REST API (FastAPI with Swagger at /docs)
- ✅ Clean banking chatbot UI

## Bonus Features Implemented

- ✅ Conversation memory (context retention across turns)
- ✅ Source citation per response
- ✅ Graceful error handling

---

## Tech Stack

| Component | Technology | Cost |
|-----------|-----------|------|
| Backend | FastAPI + Uvicorn | Free |
| Embeddings | sentence-transformers (local) | Free |
| Vector DB | ChromaDB (local) | Free |
| LLM | Groq (llama-3.3-70b) | Free tier |
| Frontend | Vanilla HTML/CSS/JS | Free |
| Deployment | Render.com | Free tier |
