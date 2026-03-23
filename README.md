# 🪽 Wings-Prompters: AI Codebase Intelligence Agent

Wings-Prompters is a high-performance, AI-driven tool designed to give engineers instant, deep insights into any GitHub repository. By combining advanced architectural mapping with Retrieval-Augmented Generation (RAG), it allows you to visualize project structures and chat directly with an AI that has "read" the entire codebase.

---

## ✨ Key Features

- **🚀 Unified Analysis**: One-click analysis that generates folder structures, identifies entry points, and maps dependencies while simultaneously indexing the repo for AI chat.
- **💬 Smart RAG Chat**: Ask complex technical questions about the repo. Powered by **Groq (Llama 3.3)** for reasoning and **Gemini** for high-dimensional code embeddings.
- **🗺️ Dependency Mapping**: Visualizes how files interact, helping you understand the complex web of imports and calls in seconds.
- **🎨 Premium UI**: A sleek, dark-mode interface with a **horizontal resizable chat panel** and real-time status tracking.
- **💾 Intelligent Persistence**: FAISS vector indices are persisted locally, so you don't have to re-index repo's you've already visited.
- **🛡️ Quota Safety Net**: Built-in fallback logic that uses architectural summaries when API limits are reached, ensuring you're never left without an answer.

---

## 🛠️ Tech Stack

- **Backend**: Python (FastAPI, Uvicorn)
- **AI/LLM**: LangChain, Groq (Llama 3.3 70B), Google Gemini (Embeddings)
- **Vector Store**: FAISS (Facebook AI Similarity Search)
- **Frontend**: Modern Vanilla JavaScript, CSS3 (Glassmorphism), Semantic HTML5
- **Data Handling**: Parallelized embedding processing with multi-key support

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- A modern web browser
- API Keys for **Groq** and **Google Gemini** (Free Tier works!)

### 1. Installation

Clone the repository:
```bash
git clone https://github.com/ManojPawar2/Wings-Prompters.git
cd Wings-Prompters
```

Install Backend Dependencies:
```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Setup

Create a `.env` file in the `backend` folder:
```env
GEMINI_API_KEY_PRIMARY=your_gemini_key_here
GEMINI_API_KEY_SECONDARY=optional_second_key_for_higher_quota
GROQ_API_KEY=your_groq_key_here
GITHUB_TOKEN=your_github_personal_access_token
```

### 3. Running the App

Start the Backend:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Open the Frontend:
Simply open `frontend/index.html` in your browser (or use VS Code "Live Server").

---

## 📖 Usage

1. **Enter URL**: Paste any public GitHub repository URL into the landing page.
2. **Analyze**: Watch as the agent maps out the tech stack, files, and dependencies.
3. **Chat**: Open the **"Ask AI"** panel on the right. Slide it to your preferred width and start asking questions like *"How does the authentication flow work?"* or *"Where is the main entry point for data processing?"*

---

## 🛡️ License
Distributed under the MIT License. See `LICENSE` for more information.

## 🤝 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

---
*Built with ❤️ for the developer community.*
