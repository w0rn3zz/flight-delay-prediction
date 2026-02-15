FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY backend/pyproject.toml .

RUN pip install --no-cache-dir uv

RUN uv sync

COPY docker/scripts/run.sh /app/run.sh
RUN chmod +x /app/run.sh

COPY backend .

EXPOSE 8000

CMD ["/app/run.sh"]
