FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /projeto_aplicado

RUN printenv > /app/build_env

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim

WORKDIR /projeto_aplicado

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY projeto_aplicado .

RUN useradd -m appuser
USER appuser

EXPOSE 8000

CMD ["fastapi", "run", "projeto_aplicado/app.py", "--host", "0.0.0.0"]