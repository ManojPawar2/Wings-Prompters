# syntax=docker/dockerfile:1
# ── NAVIgit backend image ───────────────────────────────────────────────────
# Build once, run anywhere Docker runs. API keys are NOT baked into the image —
# they are injected at runtime via --env-file / -e (see docker-compose.yml).
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# 1. Install Python dependencies first so this layer is cached unless
#    requirements.txt changes (keeps rebuilds fast).
COPY backend/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

# 2. Copy the backend application code (the app runs with app-dir = backend/).
COPY backend/ ./backend/

EXPOSE 8000

# Honor a platform-provided $PORT (Cloud Run / Render / Railway) or default 8000.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --app-dir backend"]
