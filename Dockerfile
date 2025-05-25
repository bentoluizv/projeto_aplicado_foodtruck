FROM python:3.12-slim-bookworm AS base

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

EXPOSE 8000

CMD ["uv", "run", "fastapi", "run", "projeto_aplicado/app.py"]