# 📌 Referência Rápida

## 🔗 Conectar VS Code ao Codespace

**Pelo GitHub (mais rápido):**
```
GitHub → Codespaces → [...] → Open in Visual Studio Code
```

**Pelo VS Code:**
```
Ctrl+Shift+P → "Codespaces: Connect to Codespace"
```

---

## 🌐 URLs dos Serviços

| Serviço | URL | Credenciais |
|---------|-----|-------------|
| **MLflow UI** | http://localhost:5000 | - |
| **MinIO Console** | http://localhost:9001 | user / password |

---

## 🐳 Comandos Docker

### Ver status dos containers
```bash
docker compose ps
```

### Parar todos os serviços
```bash
docker compose down
```

### Iniciar todos os serviços
```bash
docker compose up -d
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
```

### Limpar recursos não utilizados
```bash
docker system prune -a
```

---

## 🛑 Desconectar e Parar

### 1. Parar serviços (no terminal do VS Code)
```bash
docker compose down
```

### 2. Desconectar VS Code
```
Fechar VS Code ou Ctrl+Shift+P → "Close Remote Connection"
```

### 3. Parar Codespace no GitHub
```
https://github.com/codespaces → [...] → Stop codespace
```

---

## 🔍 Verificação de Saúde

### Testar MLflow
```bash
curl http://localhost:5000/health
```

### Verificar portas no VS Code
```
View → Ports (ou Ctrl+Shift+P → "Ports: Focus on Ports View")
```

---

## � Troubleshooting Rápido

### MLflow não abre
```bash
docker restart mlops-mlflow-server-1
sleep 10
curl http://localhost:5000/health
```

### Portas não funcionam
```
VS Code → Painel PORTS → Clique direito → Forward Port → Digite a porta
```

### Containers não iniciam
```bash
docker compose down
docker compose up -d
docker compose logs
```

### Codespace lento
```bash
docker system prune -a
docker compose restart
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

# 4. Trabalhar no projeto
# (editar código, executar notebooks, etc)

# 5. Ao terminar
docker compose down

# 6. Parar Codespace no GitHub
```

---

## 💡 Dicas Rápidas

✅ **Terminal do VS Code** executa comandos no Codespace

✅ **Port forwarding é automático** → acesse `localhost:porta`

✅ **Sempre execute** `docker compose down` ao terminar

✅ **Pare o Codespace** no GitHub para economizar créditos

✅ **Faça commits regularmente** → arquivos estão no Codespace

---

## 📚 Documentação

- **[README.md](./README.md)** - Documentação completa
- **[QUICKSTART.md](./QUICKSTART.md)** - Setup em 5 minutos
- **[CHECKLIST.md](./CHECKLIST.md)** - Verificação passo a passo
