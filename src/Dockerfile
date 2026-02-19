FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir uv

COPY pyproject.toml uv.lock* ./

RUN uv pip install --system --no-cache-dir .

COPY src/ ./src/

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
