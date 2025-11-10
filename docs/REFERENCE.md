# 📌 Referência Rápida — Comandos Essenciais

Comandos úteis para trabalhar com o ambiente híbrido MLOps.

---

## 🐳 Docker (VS Code do Codespace)

### Status e Logs

```bash
# Ver status de todos os containers
docker compose ps

# Ver logs de todos os serviços
docker compose logs

# Ver logs do MLflow (em tempo real)
docker compose logs -f mlflow-server

# Ver logs do MinIO
docker compose logs -f minio

# Ver logs de um serviço específico
docker logs NOME_DO_CONTAINER
```

### Gerenciar Serviços

```bash
# Iniciar todos os serviços
docker compose up -d

# Parar todos os serviços
docker compose down

# Reiniciar um serviço específico
docker compose restart mlflow-server
docker compose restart minio
docker compose restart postgres

# Reconstruir e iniciar
docker compose up -d --build

# Parar e remover volumes (limpa dados)
docker compose down -v
```

### Diagnosticar Problemas

```bash
# Ver detalhes de um container
docker inspect NOME_DO_CONTAINER

# Entrar em um container
docker exec -it mlops-mlflow-server-1 bash

# Ver uso de recursos
docker stats
```

---

## 🐍 Conda (Terminal Local)

### Gerenciar Ambientes

```bash
# Criar ambiente
conda create -n mlops-util-env python=3.13

# Ativar ambiente
conda activate mlops-util-env

# Desativar ambiente
conda deactivate

# Listar ambientes
conda env list

# Remover ambiente
conda env remove -n mlops-util-env

# Exportar ambiente
conda env export > environment.yml

# Criar ambiente a partir de arquivo
conda env create -f environment.yml
```

### Gerenciar Pacotes

```bash
# Instalar pacotes do arquivo
conda install -c conda-forge --file requirements_conda.txt

# Instalar pacote específico
conda install -c conda-forge NOME_DO_PACOTE

# Atualizar pacote
conda update NOME_DO_PACOTE

# Remover pacote
conda remove NOME_DO_PACOTE

# Listar pacotes instalados
conda list

# Buscar pacote
conda search NOME_DO_PACOTE
```

---

## 📓 Jupyter (Terminal Local)

### Kernels

```bash
# Listar kernels disponíveis
jupyter kernelspec list

# Instalar kernel do ambiente atual
python -m ipykernel install --user --name mlops-util-env --display-name "Python 3.13 (mlops-util-env)"

# Remover kernel
jupyter kernelspec uninstall mlops-util-env

# Ver onde o kernel está instalado
jupyter kernelspec list
```

### Jupyter Lab

```bash
# Iniciar Jupyter Lab
jupyter lab

# Iniciar em porta específica
jupyter lab --port 8889

# Iniciar sem abrir navegador
jupyter lab --no-browser

# Ver versão
jupyter lab --version
```

---

## 🌐 MLflow (Python)

### Configuração Básica

```python
import mlflow

# Configurar URI do servidor
mlflow.set_tracking_uri('http://localhost:5000')

# Verificar URI configurada
print(mlflow.get_tracking_uri())

# Criar/selecionar experimento
mlflow.set_experiment("meu-experimento")

# Listar experimentos
client = mlflow.MlflowClient()
experiments = client.list_experiments()
for exp in experiments:
    print(f"{exp.name} (ID: {exp.experiment_id})")
```

### Logging

```python
import mlflow

# Iniciar run
with mlflow.start_run():
    # Log de parâmetros
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("epochs", 100)
    
    # Log de métricas
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("loss", 0.05)
    
    # Log de modelo
    mlflow.sklearn.log_model(model, "model")
    
    # Log de artefato
    mlflow.log_artifact("output.txt")
```

### Consultar Runs

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Buscar runs de um experimento
experiment_id = "0"
runs = client.search_runs(experiment_id)

for run in runs:
    print(f"Run ID: {run.info.run_id}")
    print(f"Metrics: {run.data.metrics}")
    print(f"Params: {run.data.params}")
```

---

## 📡 Git (Terminal Local)

### Operações Básicas

```bash
# Ver status
git status

# Adicionar arquivos
git add .
git add ARQUIVO_ESPECIFICO

# Commit
git commit -m "Mensagem descritiva"

# Push para o fork
git push origin main

# Pull (atualizar local)
git pull origin main

# Ver histórico
git log --oneline

# Ver diferenças
git diff
```

### Branches

```bash
# Criar nova branch
git checkout -b feature/nova-funcionalidade

# Listar branches
git branch

# Mudar de branch
git checkout main

# Merge de branch
git checkout main
git merge feature/nova-funcionalidade

# Deletar branch
git branch -d feature/nova-funcionalidade
```

---

## 🔗 Codespaces (VS Code)

### Conectar/Desconectar

```
# Conectar
Ctrl+Shift+P → "Codespaces: Connect to Codespace"

# Desconectar
Ctrl+Shift+P → "Close Remote Connection"

# Recarregar janela
Ctrl+Shift+P → "Developer: Reload Window"
```

### Port Forwarding

```
# Ver portas
View → Ports

# Adicionar porta
PORTS → Forward a Port → Digite o número

# Mudar visibilidade
Clique direito na porta → Port Visibility → Public/Private

# Abrir no navegador
Clique no ícone de globo ao lado da porta
```

### Gerenciar Codespace

No GitHub (https://github.com/codespaces):

- **Stop** - Parar Codespace (libera recursos)
- **Start** - Reiniciar Codespace parado
- **Delete** - Remover Codespace permanentemente
- **Rename** - Renomear Codespace
- **Export** - Exportar dados do Codespace

---

## 🌐 Acessar Serviços

### URLs

| Serviço | URL | Credenciais |
|---------|-----|-------------|
| MLflow UI | http://localhost:5000 | - |
| MinIO Console | http://localhost:9001 | user / password |
| Postgres (MLflow) | localhost:5433 | user / password |
| Postgres (MLOps) | localhost:5434 | mlops_user / admin |

### Testar Conexões

```bash
# Testar MLflow
curl http://localhost:5000/health

# Testar MinIO
curl http://localhost:9001

# Testar Postgres (MLflow)
psql -h localhost -p 5433 -U user -d db

# Testar Postgres (MLOps)
psql -h localhost -p 5434 -U mlops_user -d mlops_db
```

---

## 🐛 Troubleshooting Rápido

### MLflow não abre

```bash
docker compose restart mlflow-server
docker compose logs mlflow-server
```

### Porta não funciona

```
VS Code Codespace → PORTS → Forward Port → 5000
```

### Conda lento

```bash
# Usar mamba (mais rápido)
conda install -c conda-forge mamba
mamba install -c conda-forge --file requirements_conda.txt
```

### Kernel não aparece

```bash
conda activate mlops-util-env
python -m ipykernel install --user --name mlops-util-env
jupyter kernelspec list
```

---

## 💡 Dicas

- ✅ Sempre ative o ambiente Conda antes de trabalhar
- ✅ Use `docker compose logs -f` para ver problemas em tempo real
- ✅ Pare o Codespace quando não estiver usando
- ✅ Faça commits frequentes para não perder trabalho
- ✅ Use dois terminais: um para Codespace, outro para local

---

📖 [README Principal](../README.md) | 🚀 [Guia Rápido](./QUICKSTART.md) | ✅ [Checklist](./CHECKLIST.md)
