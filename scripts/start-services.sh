#!/bin/bash

# Script para iniciar serviços do Docker Compose de forma ordenada
# Evita problemas de timing e dependências

set -e  # Para em caso de erro

echo "🚀 Iniciando serviços MLOps de forma ordenada..."
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para aguardar
wait_seconds() {
    local seconds=$1
    local service=$2
    echo -e "${YELLOW}⏳ Aguardando ${seconds}s para ${service} estabilizar...${NC}"
    sleep $seconds
}

# Função para verificar status
check_service() {
    local service=$1
    echo -e "${GREEN}✓ ${service} iniciado${NC}"
    docker compose ps $service
    echo ""
}

# Passo 1: Subir Minio e Postgres (infraestrutura base)
echo "📦 Passo 1/3: Iniciando Minio e Postgres..."
docker compose up -d minio postgres

wait_seconds 15 "Minio e Postgres"
check_service minio
check_service postgres

# Passo 2: Criar bucket no Minio
echo "🪣 Passo 2/3: Criando bucket no Minio..."
docker compose up -d minio-create-bucket

wait_seconds 15 "criação do bucket"
check_service minio-create-bucket

# Verificar se bucket foi criado
echo "🔍 Verificando se bucket foi criado..."
docker compose logs minio-create-bucket | tail -5

# Passo 3: Subir MLflow Server
echo "🎯 Passo 3/3: Iniciando MLflow Server..."
docker compose up -d mlflow-server

wait_seconds 15 "MLflow Server"
check_service mlflow-server

# Resumo final
echo ""
echo "=========================================="
echo "✅ Todos os serviços foram iniciados!"
echo "=========================================="
echo ""
docker compose ps
echo ""
echo "🌐 Acesse os serviços:"
echo "  - MLflow UI:    http://localhost:5000"
echo "  - MinIO Console: http://localhost:9001"
echo ""
echo "📋 Comandos úteis:"
echo "  - Ver logs:      docker compose logs -f mlflow-server"
echo "  - Parar tudo:    docker compose down"
echo "  - Restart:       ./scripts/start-services.sh"
echo ""
