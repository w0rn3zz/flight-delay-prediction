FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY backend/pyproject.toml backend/uv.lock ./

RUN uv sync --frozen --no-install-project

COPY backend/ .

COPY docker/scripts/run.sh /app/run.sh
RUN chmod +x /app/run.sh

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["/app/run.sh"]
