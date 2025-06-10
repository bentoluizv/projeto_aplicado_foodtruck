ARG BASE_IMAGE=python:3.12-slim-bookworm

FROM ${BASE_IMAGE} AS base

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

FROM base AS builder

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv venv && . .venv/bin/activate && \
    uv lock && \
    uv sync

COPY . .

FROM base AS runner

WORKDIR /app

COPY --from=builder /app/.venv .venv

ENV PATH="/app/.venv/bin:$PATH"

COPY --from=builder /app/projeto_aplicado /app/projeto_aplicado
COPY --from=builder /app/migrations /app/migrations
COPY --from=builder /app/pyproject.toml /app/pyproject.toml
COPY --from=builder /app/uv.lock /app/uv.lock
COPY --from=builder /app/alembic.ini /app/alembic.ini

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/docs || exit 1

ENTRYPOINT ["uvicorn"]

CMD ["projeto_aplicado.app:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
