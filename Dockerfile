FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_ENV=production
ENV APP_DB_PATH=/data/my_ration.sqlite3

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY docs ./docs
COPY README.md ./README.md

RUN mkdir -p /data \
    && useradd -m appuser \
    && chown -R appuser:appuser /app /data

USER appuser

EXPOSE 8550

CMD ["flet", "run", "--web", "--host", "0.0.0.0", "--port", "8550", "app/main.py"]

