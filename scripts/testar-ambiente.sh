#!/usr/bin/env bash
# Verifica se o ambiente do aluno consegue subir os serviços do projeto.
#
# Uso (na raiz do projeto):
#   bash scripts/testar-ambiente.sh          # sobe os serviços e testa
#   bash scripts/testar-ambiente.sh --down   # testa e derruba os serviços no final
#
# Funciona em macOS, Linux e Windows (via WSL).

set -u
cd "$(dirname "$0")/.." || exit 1

MLFLOW_PORT=5010
PORTS=(5010 5433 9000)
FALHAS=0

ok()    { printf "  \033[32m[OK]\033[0m %s\n" "$1"; }
aviso() { printf "  \033[33m[AVISO]\033[0m %s\n" "$1"; }
erro()  { printf "  \033[31m[ERRO]\033[0m %s\n" "$1"; FALHAS=$((FALHAS + 1)); }
titulo(){ printf "\n\033[1m%s\033[0m\n" "$1"; }

porta_em_uso() { (echo > "/dev/tcp/127.0.0.1/$1") >/dev/null 2>&1; }

titulo "1. Docker"
if ! command -v docker >/dev/null 2>&1; then
  erro "Docker não encontrado. Instale o Docker Desktop: https://www.docker.com/products/docker-desktop/"
  exit 1
fi
ok "docker instalado ($(docker --version | cut -d, -f1))"

if ! docker info >/dev/null 2>&1; then
  erro "O Docker não está rodando. Abra o Docker Desktop e aguarde ele iniciar."
  exit 1
fi
ok "Docker daemon rodando"

if ! docker compose version >/dev/null 2>&1; then
  erro "'docker compose' (v2) não disponível. Atualize o Docker Desktop."
  exit 1
fi
ok "docker compose disponível ($(docker compose version --short))"

titulo "2. Arquivo .env"
if [ -f .env ]; then
  ok ".env encontrado"
else
  erro "Arquivo .env não existe. Rode: cp .env.example .env"
  aviso "Sem o .env, os notebooks gravam no MLflow local (pasta mlruns/) e nada aparece na UI."
fi

titulo "3. Portas livres (${PORTS[*]})"
EM_EXECUCAO=$(docker compose ps --status running -q 2>/dev/null | wc -l | tr -d ' ')
if [ "$EM_EXECUCAO" -gt 0 ]; then
  ok "Serviços do projeto já estão rodando; pulando verificação de portas"
else
  PORTAS_OCUPADAS=0
  for p in "${PORTS[@]}"; do
    if porta_em_uso "$p"; then
      erro "Porta $p já está em uso por outro programa. Descubra qual com: lsof -i :$p (macOS/Linux) ou netstat -ano | findstr :$p (Windows)"
      PORTAS_OCUPADAS=1
    else
      ok "porta $p livre"
    fi
  done
  if [ "$PORTAS_OCUPADAS" -gt 0 ]; then
    erro "Corrija os erros acima antes de subir os serviços."
    exit 1
  fi
fi

titulo "4. Subindo os serviços (o primeiro build pode levar alguns minutos)"
if ! docker compose up -d --build --wait --wait-timeout 300; then
  erro "docker compose up falhou. Status dos containers:"
  docker compose ps -a
fi

titulo "5. MLflow server"
STATUS=000
for _ in $(seq 1 60); do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:${MLFLOW_PORT}/health" || true)
  [ "$STATUS" = "200" ] && break
  sleep 2
done
RESTARTS=$(docker inspect "$(docker compose ps -q mlflow-server)" --format '{{.RestartCount}}' 2>/dev/null || echo "?")
if [ "$STATUS" = "200" ] && [ "$RESTARTS" = "0" ]; then
  ok "MLflow respondendo em http://localhost:${MLFLOW_PORT}"
else
  erro "MLflow não respondeu (HTTP $STATUS, reinícios: $RESTARTS). Últimas linhas do log:"
  docker compose logs --tail 30 mlflow-server
fi

titulo "6. Bucket S3 (cloudserver)"
BUCKET_EXIT=$(docker inspect "$(docker compose ps -a -q cloudserver-create-bucket)" --format '{{.State.ExitCode}}' 2>/dev/null || echo "?")
if [ "$BUCKET_EXIT" = "0" ]; then
  ok "bucket s3://bucket criado"
else
  erro "Criação do bucket falhou (exit $BUCKET_EXIT):"
  docker compose logs --tail 20 cloudserver-create-bucket
fi

titulo "7. Teste ponta a ponta (registrar run + artefato no MLflow)"
PY=""
for cand in python python3; do
  if command -v "$cand" >/dev/null 2>&1 && "$cand" -c "import mlflow, boto3, dotenv" >/dev/null 2>&1; then
    PY=$cand; break
  fi
done
if [ -z "$PY" ]; then
  aviso "Python com mlflow/boto3/python-dotenv não encontrado. Ative o ambiente (conda activate mlops-util-env) e rode de novo para este teste."
elif [ "$STATUS" = "200" ]; then
  if MLFLOW_DISABLE_AGENT_HINT=1 "$PY" - <<'EOF'
import os, sys, tempfile, mlflow
from dotenv import load_dotenv
load_dotenv(".env")
uri = os.getenv("MLFLOW_TRACKING_URI")
if not uri:
    sys.exit("MLFLOW_TRACKING_URI não definido (verifique o .env)")
mlflow.set_tracking_uri(uri)
mlflow.set_experiment("teste-ambiente")
with mlflow.start_run(run_name="teste-ambiente") as run:
    mlflow.log_param("ok", 1)
    mlflow.log_metric("ok", 1.0)
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "teste.txt")
        open(p, "w").write("ok")
        mlflow.log_artifact(p)
arts = [a.path for a in mlflow.MlflowClient().list_artifacts(run.info.run_id)]
assert "teste.txt" in arts, f"artefato não encontrado: {arts}"
print(f"     run {run.info.run_id} -> {run.info.artifact_uri}")
EOF
  then
    ok "run e artefato registrados no MLflow/S3"
  else
    erro "Falha ao registrar no MLflow (veja a mensagem acima)."
  fi
fi

if [ "${1:-}" = "--down" ]; then
  titulo "Derrubando os serviços"
  docker compose down
fi

titulo "Resultado"
if [ "$FALHAS" -eq 0 ]; then
  printf "  \033[32mAmbiente pronto!\033[0m MLflow UI: http://localhost:%s\n" "$MLFLOW_PORT"
else
  printf "  \033[31m%d problema(s) encontrado(s).\033[0m Veja as mensagens acima.\n" "$FALHAS"
  exit 1
fi
