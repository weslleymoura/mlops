# 📌 Referência Rápida - Comandos Essenciais

## 🔗 Conectar VS Code Local ao Codespace

```plaintext
VS Code → Ctrl+Shift+P → "Codespaces: Connect to Codespace"
```

ou

```plaintext
GitHub → Codespaces → [...] → Open in Visual Studio Code
```

---

## 🐳 Docker - Gerenciamento de Containers

### Ver status dos containers
```bash
docker compose ps
```

### Iniciar todos os serviços
```bash
docker compose up -d
```

### Parar todos os serviços
```bash
docker compose down
```

### Reiniciar todos os serviços
```bash
docker compose restart
```

### Reiniciar apenas o MLflow
```bash
docker restart mlops-mlflow-server-1
```

### Ver logs em tempo real
```bash
# MLflow
docker logs -f mlops-mlflow-server-1

# Todos os serviços
docker compose logs -f

# Serviço específico
docker compose logs -f mlflow-server
```

### Reconstruir imagens
```bash
docker compose up -d --build
```

### Limpar recursos não utilizados
```bash
docker system prune -a
```

---

## 🌐 URLs dos Serviços

| Serviço | URL | Credenciais |
|---------|-----|-------------|
| **MLflow UI** | http://localhost:5000 | - |
| **MinIO Console** | http://localhost:9001 | user / password |
| **MinIO API** | http://localhost:9000 | - |
| **Postgres (MLflow)** | localhost:5433 | user / password / db |
| **Postgres (MLOps)** | localhost:5434 | mlops_user / admin / mlops_db |

---

## 🐍 Python - Ambiente Virtual

### Ativar ambiente virtual (se local)
```bash
# Linux/Mac
source mlops-util-env/bin/activate

# Windows
mlops-util-env\Scripts\activate
```

### Desativar ambiente virtual
```bash
deactivate
```

### Instalar/Atualizar dependências
```bash
pip install -r requirements.txt
pip install --upgrade -r requirements.txt
```

---

## 📓 Jupyter Notebook

### Executar notebook
```bash
jupyter notebook notebooks/example_mlflow.ipynb
```

### Listar kernels disponíveis
```bash
jupyter kernelspec list
```

---

## 🔍 Verificação de Saúde

### Testar MLflow
```bash
curl http://localhost:5000/health
```

### Testar MinIO
```bash
curl http://localhost:9000/minio/health/live
```

### Verificar portas em uso
```bash
# Linux/Mac
netstat -tuln | grep LISTEN

# No Codespace
docker compose ps
```

---

## 🛑 Parar/Gerenciar Codespace

### Pelo VS Code
```plaintext
Ctrl+Shift+P → "Codespaces: Stop Current Codespace"
Ctrl+Shift+P → "Codespaces: Disconnect"
```

### Pelo GitHub
```plaintext
https://github.com/codespaces
[...] → Stop codespace
[...] → Delete
```

### Parar serviços antes de parar o Codespace
```bash
docker compose down
```

---

## 🔧 Troubleshooting Rápido

### MLflow não abre (localhost:5000)
```bash
docker restart mlops-mlflow-server-1
sleep 10
curl http://localhost:5000/health
```

### Portas não encaminhadas
```plaintext
VS Code → Painel PORTS → Clique direito → Forward Port → Digite a porta
```

### Containers não iniciam
```bash
docker compose down
docker compose up -d
docker compose ps
docker compose logs
```

### Codespace lento
```bash
# Limpar cache Docker
docker system prune -a

# Reiniciar serviços
docker compose down && docker compose up -d
```

### Espaço em disco cheio
```bash
# Ver uso
docker system df

# Limpar
docker system prune -a --volumes
```

---

## 📊 Monitoramento

### Ver uso de recursos dos containers
```bash
docker stats
```

### Ver espaço em disco
```bash
df -h
docker system df
```

### Ver processos em execução
```bash
ps aux | grep -E 'mlflow|docker'
```

---

## 🔐 Variáveis de Ambiente (para scripts)

```bash
# Para conectar ao MLflow
export MLFLOW_TRACKING_URI=http://localhost:5000

# Para acessar MinIO (S3)
export AWS_ACCESS_KEY_ID=user
export AWS_SECRET_ACCESS_KEY=password
export MLFLOW_S3_ENDPOINT_URL=http://localhost:9000
```

---

## 🎯 Workflow Típico

```bash
# 1. Conectar VS Code ao Codespace
# (Ctrl+Shift+P → "Codespaces: Connect to Codespace")

# 2. Verificar serviços
docker compose ps

# 3. Se não estiverem rodando
docker compose up -d

# 4. Abrir MLflow no navegador
# http://localhost:5000

# 5. Trabalhar no projeto
# (editar código, executar notebooks, etc)

# 6. Ao terminar
docker compose down

# 7. Parar Codespace no GitHub
# (https://github.com/codespaces → [...] → Stop)
```

---

## 📚 Links Úteis

- **Documentação Completa**: [README.md](./README.md)
- **Guia Rápido**: [QUICKSTART.md](./QUICKSTART.md)
- **Checklist**: [CHECKLIST.md](./CHECKLIST.md)
- **MLflow Docs**: https://mlflow.org/docs/latest/
- **GitHub Codespaces**: https://github.com/features/codespaces

---

## 💡 Dicas Rápidas

✅ **Use o terminal do VS Code** - Ele executa comandos no Codespace automaticamente

✅ **Port forwarding é automático** - Basta acessar `localhost:porta`

✅ **Sempre execute `docker compose down`** - Economiza créditos do GitHub

✅ **Verifique o painel PORTS** - Para ver todas as portas encaminhadas

✅ **Use `docker compose ps`** - Para verificar o status dos serviços

✅ **Salve seu trabalho** - Faça commits regularmente, os arquivos estão no Codespace

---

**Última atualização**: 08/11/2025
