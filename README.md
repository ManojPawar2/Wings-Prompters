# Wings-Prompters: Codebase Intelligence Agent

**AI-Powered System for Understanding Large Code Repositories**

## The Hackathon Challenge
**Scenario:**
Imagine joining a startup as a new developer. Last week, the senior developer quit, leaving behind a 40,000-line production repository with zero documentation and an urgent bug report waiting in your inbox. Where do you even begin?

**The Problem:**
Modern software projects contain large and complex codebases with deeply nested folders, multiple modules, and hidden dependencies. When developers join a new project, contribute to open source, or debug legacy applications, they waste significant time trying to understand:
- The overall tech stack and architecture.
- The main entry points and execution flow.
- The complex web of file dependencies.

---

## The Solution: Wings-Prompters
Wings-Prompters is a high-performance, AI-driven assistant designed to eliminate the "onboarding bottleneck." By combining automated architectural mapping with Retrieval-Augmented Generation (RAG), it allows developers to visualize project structures and chat directly with an AI that has analyzed the entire codebase in seconds.

### Key Features
- **Architectural Analysis**: Automatic generation of folder structures, entry point identification, and technology stack detection.
- **RAG-Powered Chat**: An interactive AI chat panel (powered by Groq Llama 3.3 and Gemini Embeddings) that provides grounded answers with source file citations.
- **Dependency Mapping**: Visualizes the relationship between files to help trace data flow and imports.
- **Resizable Interface**: A flexible, modern UI featuring a draggable chat panel for an optimized development workflow.
- **Local Persistence**: FAISS vector indices are stored locally for fast, recurring access to previously analyzed repositories.

---

## Technical Architecture
- **Backend**: FastAPI (Python) handles repository ingestion, multi-threaded embedding processing, and RAG orchestration.
- **AI Engine**: 
    - **Groq (Llama 3.3 70B)**: Deep technical reasoning and code analysis.
    - **Google Gemini**: High-performance vector embeddings.
- **Vector Store**: FAISS (Facebook AI Similarity Search) for optimized document retrieval.
- **Frontend**: A sleek, accessible interface built with modern Vanilla JavaScript and CSS3.

---

## Getting Started

### Prerequisites
- Python 3.9+
- API Keys for **Groq** and **Google Gemini** (Free Tier)

### 1. Installation
```bash
git clone https://github.com/ManojPawar2/Wings-Prompters.git
cd Wings-Prompters/backend
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file in the `backend` directory:
```env
GEMINI_API_KEY_PRIMARY=your_key_here
GEMINI_API_KEY_SECONDARY=additional_key_for_quota (optional)
GROQ_API_KEY=your_key_here
GITHUB_TOKEN=your_token_here
```

### 3. Execution
Start the backend server:
```bash
uvicorn app.main:app --reload --port 8000
```
Open `frontend/index.html` in your browser to begin analysis.

---

## Project Impact
Wings-Prompters reduces the time spent on "code discovery" by up to 80%, allowing developers to focus on writing code and fixing bugs rather than deciphering complex file systems. It is the ultimate tool for rapid onboarding and legacy codebase maintenance.

---
*Developed for the Codebase Intelligence Hackathon.*
