# AI Codebase Intelligence Platform

An AI-powered developer tool for intelligent code search, automated repository indexing, and AI-driven code explanations. Clone any GitHub repository, index it into a vector database, and interact with your codebase using natural language.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688)
![Next.js](https://img.shields.io/badge/Next.js-16-black)
![Groq](https://img.shields.io/badge/Groq-Llama_3.3_70B-orange)

---

## Features

- **AI Q&A** — Ask natural language questions about your codebase and get intelligent answers with source references
- **GitHub Integration** — Clone and index any GitHub repository in one step
- **Semantic Code Search** — Find relevant code using natural language queries powered by vector similarity search
- **AI Code Explainer** — Paste any code snippet and get a clear, detailed explanation
- **RAG Pipeline** — Retrieval-Augmented Generation using FAISS vector store and sentence-transformers embeddings
- **Modern Frontend** — Dark-themed Next.js UI with sidebar navigation

## Tech Stack

| Layer            | Technology                               |
| ---------------- | ---------------------------------------- |
| **LLM**          | Groq API + Llama 3.3 70B Versatile       |
| **Embeddings**   | sentence-transformers (all-MiniLM-L6-v2) |
| **Vector Store** | FAISS (faiss-cpu)                        |
| **Backend**      | Python 3.12, FastAPI, Uvicorn            |
| **Frontend**     | Next.js 16, React 19, Tailwind CSS 4     |
| **Automation**   | n8n workflows (optional)                 |

## Project Structure

```
├── backend/                  # FastAPI backend
│   ├── main.py               # App entry point
│   ├── routes/               # API endpoints
│   │   ├── ask.py            # POST /api/ask
│   │   ├── index.py          # POST /api/index-repo
│   │   ├── github.py         # GitHub clone/index/list/delete
│   │   ├── code_intelligence.py  # Search & explain
│   │   └── slack.py          # Slack integration
│   ├── services/             # Business logic
│   │   ├── rag_service.py    # Groq LLM + RAG
│   │   ├── github_service.py # Git operations
│   │   └── code_intelligence_service.py
│   ├── rag/                  # RAG pipeline
│   │   ├── embeddings.py     # Sentence-transformer embeddings
│   │   ├── vector_store.py   # FAISS save/load
│   │   ├── retriever.py      # Similarity search
│   │   ├── code_chunker.py   # Code splitting
│   │   ├── repo_loader.py    # File loading
│   │   └── rag_pipeline.py   # Indexing pipeline
│   └── schemas/              # Pydantic models
├── frontend/                 # Next.js frontend
│   └── app/
│       ├── page.tsx          # Ask AI page
│       ├── repos/page.tsx    # GitHub repos management
│       ├── search/page.tsx   # Semantic code search
│       ├── explain/page.tsx  # AI code explainer
│       ├── components/       # Sidebar, shared UI
│       └── lib/api.ts        # API client
├── scripts/                  # CLI utilities
│   ├── clone_repo.py         # Clone repos from terminal
│   ├── index_repo.py         # Index repos from terminal
│   └── test_query.py         # Test AI queries
├── automation/               # n8n workflow configs
│   ├── github_auto_index.json
│   └── slack_ai_assistant.json
└── data/                     # Runtime data
    ├── repos/                # Cloned repositories
    ├── vector_store/         # FAISS index files
    └── embedding_cache/      # Cached embeddings
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- [Groq API key](https://console.groq.com/) (free)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Codebase-Intelligence-Platform.git
cd AI-Codebase-Intelligence-Platform
```

### 2. Set up the backend

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure environment variables

Create `backend/.env`:

```env
GROQ_API_KEY=your_groq_api_key_here
VECTOR_DB_PATH=../data/vector_store
REPO_PATH=../data/repos
```

### 4. Start the backend

```bash
cd backend
uvicorn main:app --reload
```

Backend runs at **http://localhost:8000** — Swagger docs at `/docs`.

### 5. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at **http://localhost:3000**.

## API Endpoints

| Method   | Endpoint                      | Description                        |
| -------- | ----------------------------- | ---------------------------------- |
| `POST`   | `/api/ask`                    | Ask a question about indexed code  |
| `POST`   | `/api/index-repo`             | Index a local or GitHub repository |
| `POST`   | `/api/github/clone`           | Clone a GitHub repository          |
| `POST`   | `/api/github/clone-and-index` | Clone + index in one step          |
| `GET`    | `/api/github/repos`           | List all indexed repositories      |
| `DELETE` | `/api/github/repos/{name}`    | Delete a repository                |
| `POST`   | `/api/search`                 | Semantic code search               |
| `POST`   | `/api/explain`                | AI code explanation                |

## Usage

### Index a GitHub repo

```bash
curl -X POST http://localhost:8000/api/github/clone-and-index \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/user/repo"}'
```

### Ask a question

```bash
curl -X POST http://localhost:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "How does the authentication system work?"}'
```

### Search code

```bash
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "database connection handling", "k": 5}'
```

### Explain code

```bash
curl -X POST http://localhost:8000/api/explain \
  -H "Content-Type: application/json" \
  -d '{"code": "def factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)", "language": "python"}'
```

## CLI Scripts

```bash
# Clone a repo
python scripts/clone_repo.py https://github.com/user/repo

# Index a repo
python scripts/index_repo.py https://github.com/user/repo

# Test a query
python scripts/test_query.py "What does the main function do?"
```

## License

MIT
