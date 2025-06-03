FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder
WORKDIR /app

COPY ./pyproject.toml ./alembic.ini ./deploy/url_alias/entrypoint.sh ./
COPY ./src ./src

RUN uv sync --no-cache


FROM python:3.13-slim as final
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="/app/.venv/bin" \
    PATH="/app/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y curl


COPY --from=builder /app/ ./

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
