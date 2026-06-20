"""
Centralised configuration — loads environment variables once and exposes them
as module-level constants.  All secrets stay in .env; nothing is hard-coded.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load backend/.env by absolute path (this file is backend/app/config.py, so the
# .env sits two levels up). Without this, running uvicorn from the project root
# would search the wrong directory and silently load no keys. override=True lets
# the .env win over any stale/empty shell environment variables.
_ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_ENV_PATH, override=True)

GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")

# LLM Providers
GEMINI_API_KEY_PRIMARY: str = (
    os.getenv("GEMINI_API_KEY_PRIMARY")
    or os.getenv("GEMINI_API_KEY_RAG")
    or os.getenv("GEMINI_API_KEY", "")
)
GEMINI_API_KEY_SECONDARY: str = os.getenv("GEMINI_API_KEY_SECONDARY", "")

# Groq — primary + secondary for quota/rate-limit failover (mirrors Gemini).
GROQ_API_KEY_PRIMARY: str = (
    os.getenv("GROQ_API_KEY_PRIMARY")
    or os.getenv("GROQ_API_KEY")
    or os.getenv("GROQ_API_KEY_RAG", "")
)
GROQ_API_KEY_SECONDARY: str = os.getenv("GROQ_API_KEY_SECONDARY", "")

# Backward-compat alias: older modules import GROQ_API_KEY directly.
GROQ_API_KEY: str = GROQ_API_KEY_PRIMARY

# ── Tunables ────────────────────────────────────────────────────────────────
MAX_FILES_TO_PROCESS: int = 500          # cap after priority scoring
GITHUB_REQUEST_TIMEOUT: float = 60.0     # seconds per GitHub API call
LLM_REQUEST_TIMEOUT: float = 45.0        # per-provider timeout; fail over fast if one stalls
MAX_FILE_SIZE_BYTES: int = 500_000       # skip files larger than ~500 KB

# ── LLM Configuration ──────────────────────────────────────────────────────
GEMINI_MODEL: str = "gemini-2.5-flash"
GROQ_MODEL: str = "llama-3.1-8b-instant"

# ── Allowed extensions ──────────────────────────────────────────────────────
ALLOWED_EXTENSIONS: set[str] = {
    ".js", ".ts", ".jsx", ".tsx",
    ".py",
    ".java",
}

# ── Ignored directories ────────────────────────────────────────────────────
IGNORED_DIRS: set[str] = {
    "node_modules", "dist", "build", ".git", ".venv",
    "__pycache__", ".next", "out", ".tox", ".mypy_cache",
    "vendor", "target", ".gradle",
}
