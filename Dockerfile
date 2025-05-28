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

# Copy all necessary project files
COPY --from=builder /app/projeto_aplicado /app/projeto_aplicado
COPY --from=builder /app/migrations /app/migrations
COPY --from=builder /app/pyproject.toml /app/pyproject.toml
COPY --from=builder /app/uv.lock /app/uv.lock
COPY --from=builder /app/alembic.ini /app/alembic.ini

# Create startup script
RUN echo '#!/bin/bash\n\
echo "Waiting for postgres..."\n\
while ! nc -z postgres 5432; do\n\
  sleep 0.1\n\
done\n\
echo "PostgreSQL started"\n\
\n\
echo "Initializing database..."\n\
python -m projeto_aplicado.scripts.init_db\n\
\n\
echo "Starting application..."\n\
uv run fastapi run projeto_aplicado/app.py\n\
' > /app/start.sh && chmod +x /app/start.sh

# Install netcat for the wait script
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

EXPOSE 8000

CMD ["/app/start.sh"]