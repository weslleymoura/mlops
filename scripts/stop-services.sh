#!/bin/bash

# Script para parar serviços do Docker Compose de forma ordenada

set -e

echo "🛑 Parando serviços MLOps de forma ordenada..."
echo ""

# Cores
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Passo 1: Parar MLflow (primeiro serviço que depende dos outros)
echo -e "${YELLOW}📉 Passo 1/3: Parando MLflow Server...${NC}"
docker compose stop mlflow-server
echo -e "✓ MLflow Server parado"
echo ""

# Passo 2: Parar Minio e Postgres
echo -e "${YELLOW}📉 Passo 2/3: Parando Minio e Postgres...${NC}"
docker compose stop minio postgres
echo -e "✓ Minio e Postgres parados"
echo ""

# Passo 3: Remover containers auxiliares
echo -e "${YELLOW}🗑️  Passo 3/3: Limpando containers auxiliares...${NC}"
docker compose rm -f minio-create-bucket
echo -e "✓ Containers auxiliares removidos"
echo ""

echo "=========================================="
echo -e "${RED}✅ Todos os serviços foram parados!${NC}"
echo "=========================================="
echo ""
docker compose ps
echo ""
echo "📋 Para reiniciar:"
echo "  ./scripts/start-services.sh"
echo ""
echo "🗑️  Para limpar completamente (remove volumes):"
echo "  docker compose down -v"
echo ""
