# syntax=docker/dockerfile:1
FROM python:3.11-slim

# Set metadata
LABEL maintainer="Plant Disease Detection Project"
LABEL description="AI-powered plant disease classification & treatment recommendation"

# Set working directory inside container
WORKDIR /app

# ── System dependencies ──────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ── Python dependencies ──────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Application code ─────────────────────────────────────────────────
COPY . .

# Create necessary runtime directories
RUN mkdir -p app/static/uploads models/saved_model logs/tensorboard

# ── Environment Variables ────────────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    FLASK_APP=app/app.py \
    PORT=8000

# ── Expose Flask port ────────────────────────────────────────────────
EXPOSE 8000

# ── Health check ─────────────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1

# ── Run command ──────────────────────────────────────────────────────
CMD ["python", "app/app.py"]

