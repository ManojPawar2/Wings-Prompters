# NAVIgit: Codebase Intelligence Agent

**AI-Powered System for Understanding Large Code Repositories**

NAVIgit analyses any public GitHub repository and returns structured architectural
intelligence — folder explanations (M1), entry-point detection with execution flow
(M2), and a file-level dependency graph (M3) — plus a RAG-powered chat that answers
grounded questions about the codebase with source citations.

---

## The Solution
By combining automated architectural mapping with Retrieval-Augmented Generation
(RAG), NAVIgit lets developers visualise project structure and chat directly with an
AI that has analysed the entire codebase in seconds.

### Key Features
- **Architectural Analysis** — folder structure, entry-point detection, tech-stack inference.
- **RAG-Powered Chat** — grounded answers with source file citations (Groq Llama 3.3 + Gemini embeddings + FAISS).
- **Dependency Mapping** — visualises file relationships to trace data flow and imports.
- **Provider Failover** — Gemini → Groq with primary/secondary keys, so a quota/rate-limit on one key automatically falls over to the next.

---

## Technical Architecture
- **Backend** — FastAPI (Python 3.11). A **single** service exposes both the analysis
  endpoints (`/process-repo`, `/chat`) and the RAG endpoints (`/rag/index`, `/rag/chat`, `/rag/status`).
- **AI Engine**
    - **Groq (Llama 3.1 / 3.3)** — technical reasoning, code analysis, and RAG answers.
    - **Google Gemini** — vector embeddings (`gemini-embedding-001`).
- **Vector Store** — FAISS (in-memory, rebuilt per repository; persisted to `faiss_index/`).
- **Frontend** — static HTML / vanilla JS / CSS (no build step).

```
frontend/  → static UI (Vercel / Netlify / any static host)
backend/   → FastAPI app  (app.main:app, run with --app-dir backend)
Dockerfile, docker-compose.yml → containerised backend + frontend
```

---

## Getting Started (local)

### Prerequisites
- **Python 3.11**
- Free API keys: **Google Gemini** (https://aistudio.google.com/apikey) and **Groq** (https://console.groq.com/keys)
- A **GitHub token** (classic, `public_repo` scope) — https://github.com/settings/tokens

### 1. Install
```bash
git clone https://github.com/ManojPawar2/Wings-Prompters.git
cd Wings-Prompters
python -m venv .venv
# Windows:
.\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
# macOS/Linux:
# ./.venv/bin/pip install -r backend/requirements.txt
```

### 2. Configure environment
Create **`backend/.env`** (this file is git-ignored — never commit it):
```env
GEMINI_API_KEY_PRIMARY=your_key
GEMINI_API_KEY_SECONDARY=your_second_key   # optional, for quota failover
GROQ_API_KEY_PRIMARY=your_key
GROQ_API_KEY_SECONDARY=your_second_key      # optional, for quota failover
GITHUB_TOKEN=your_token
```
> The backend loads `backend/.env` by absolute path, so it works no matter which
> directory you launch from. The legacy single-key names (`GROQ_API_KEY`,
> `GEMINI_API_KEY`) are still honoured as fallbacks.

### 3. Run
**Backend** (terminal 1):
```bash
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000 --app-dir backend
```
**Frontend** (terminal 2):
```bash
.\.venv\Scripts\python.exe -m http.server 5500 --directory frontend
```
Open **http://localhost:5500/index.html**. The frontend auto-detects `localhost` and
talks to the backend on `http://127.0.0.1:8000`.

---

## Run with Docker

The backend is containerised; secrets are injected at runtime (never baked into the image).

```bash
# from the repo root — builds the image and runs backend (:8000) + frontend (:5500)
docker compose up --build
```
Open **http://localhost:5500/index.html**. `docker-compose.yml` reads your keys from
`backend/.env` via `env_file`.

**Move the image to another machine** (build once, run anywhere):
```bash
docker save navigit-backend:latest -o navigit.tar     # on machine A
# copy navigit.tar AND backend/.env to machine B, then:
docker load -i navigit.tar                             # on machine B
docker compose up
```
> The image is CPU-arch specific (build on, or rebuild for, the same x86-64 / arm64
> target). The FAISS index and your `.env` are **not** in the image — provide the
> `.env` and re-index on the new machine.

---

## Deployment (free tiers)

This is a split deploy: **static frontend** on one host, **backend** on another
(the backend needs real RAM + long requests, which static/serverless hosts can't give).

### Frontend → Vercel / Netlify / Cloudflare Pages (static, free)
Deploy the `frontend/` folder. Then point it at your backend by setting `PROD_BACKEND`
in `frontend/index.html` (the inline config block near the bottom):
```js
const PROD_BACKEND = 'https://your-backend-url';   // your backend's public HTTPS URL
```
You can also retarget the live site **without redeploying** via a query param:
`https://<your-site>/?api=https://your-backend-url`. CORS is already open (`allow_origins=["*"]`).

### Backend → pick one
- **Cloudflare Tunnel (quick demo, laptop-hosted):** run the backend locally, then
  `cloudflared tunnel --url http://localhost:8000` → gives a public HTTPS URL that
  forwards to your container. URL changes on restart; laptop must stay on.
- **Hugging Face Spaces (always-on, recommended):** Docker SDK Space, 16 GB free RAM,
  permanent `https://<user>-<name>.hf.space` URL. Add the same Docker image, set the 5
  keys as Space **Secrets**, bind port `7860`.

> ⚠️ The in-memory FAISS index is wiped on any restart/sleep/redeploy — re-run
> `POST /rag/index` (or have the frontend re-index on demand) after a cold start.

---

## API Endpoints
| Method | Path | Purpose |
|---|---|---|
| `GET`  | `/health` | Liveness check |
| `POST` | `/process-repo` | Analyse a repo → M1 / M2 / M3 |
| `POST` | `/chat` | Lightweight repo Q&A |
| `POST` | `/rag/index` | Build the FAISS index for a repo |
| `POST` | `/rag/chat` | Grounded RAG answer (modes B1 / B2 / B3) |
| `GET`  | `/rag/status` | Is a repo indexed? |

Interactive docs at `http://localhost:8000/docs`.

---

*Developed by **Team Prompters** for the Codebase Intelligence Hackathon.*
