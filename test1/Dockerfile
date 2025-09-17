# Multi-stage Dockerfile for pypelines (Python 3.13)

# Builder stage: create wheels
FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install build deps
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential gcc git \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install build tools
RUN pip install --upgrade pip build wheel setuptools

# Copy project metadata and source
COPY pyproject.toml setup.cfg* .  
COPY src ./src

# Build wheel(s)
RUN python -m build --wheel --outdir /wheels .

# Runtime stage
FROM python:3.13-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install runtime deps from built wheel(s)
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*.whl

# Copy source (useful for mounts in dev; not required after wheel install)
COPY src ./src
COPY pyproject.toml ./

EXPOSE 8000

# Default command: start uvicorn serving the app
CMD ["uvicorn", "pypelines.main:app", "--host", "0.0.0.0", "--port", "8000"]
