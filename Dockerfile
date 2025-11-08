FROM python:3.13-slim

WORKDIR /app

# Instala dependências necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir mlflow boto3 psycopg2-binary

COPY . /app
CMD ["bash"]