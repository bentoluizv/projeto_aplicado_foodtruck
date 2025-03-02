FROM python:3.13-slim AS builder

ARG ENV
ARG DEBUG
ARG DATABASE_URL
ARG REDIS_URL
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB

ENV ENV=$ENV
ENV DEBUG=$DEBUG
ENV DATABASE_URL=$DATABASE_URL
ENV REDIS_URL=$REDIS_URL
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_DB=$POSTGRES_DB

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN printenv > /app/build_env

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app/build_env .env

COPY projeto_aplicado .

RUN useradd -m appuser
USER appuser

EXPOSE 8000

CMD ["fastapi", "run", "projeto_aplicado/app.py", "--host", "0.0.0.0"]