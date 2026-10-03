FROM python:3.13-slim

WORKDIR /app

# Instala dependências necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Versões fixadas para que todos os alunos tenham o mesmo ambiente
RUN pip install --no-cache-dir mlflow==3.16.1 boto3==1.43.108 psycopg2-binary==2.9.13

COPY . /app
CMD ["bash"]