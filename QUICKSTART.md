# 🚀 Guia Rápido: VS Code Local + GitHub Codespace

## 📋 Pré-requisitos (5 minutos)

1. ✅ Conta no GitHub
2. ✅ VS Code instalado ([Download](https://code.visualstudio.com/))
3. ✅ Extensão **GitHub Codespaces** no VS Code

## 🎯 Setup Completo em 3 Passos

### Passo 1️⃣: Criar o Codespace (2 minutos)

```
GitHub → Este Repo → Code → Codespaces → Create codespace on main
```

Aguarde a criação. O ambiente iniciará automaticamente:
- ✅ Python 3.13
- ✅ Docker Compose
- ✅ MLflow, MinIO, Postgres

### Passo 2️⃣: Conectar VS Code Local (1 minuto)

**Opção A: Pelo VS Code**
```
VS Code → Ctrl+Shift+P → "Codespaces: Connect to Codespace" → Selecione o codespace
```

**Opção B: Pelo GitHub**
```
GitHub → Codespaces → [...] → Open in Visual Studio Code
```

### Passo 3️⃣: Verificar Portas (30 segundos)

No VS Code, abra o painel **PORTS** (View → Ports):

| Porta | Serviço | URL |
|-------|---------|-----|
| 5000 | MLflow UI | http://localhost:5000 |
| 9001 | MinIO Console | http://localhost:9001 |
| 5433 | Postgres (MLflow) | localhost:5433 |
| 5434 | Postgres (MLOps) | localhost:5434 |

## ✨ Pronto! Agora você pode:

### 1. Acessar o MLflow
```bash
# No navegador local:
http://localhost:5000
```

### 2. Executar o Notebook de Exemplo
```bash
# No terminal do VS Code (conectado ao Codespace):
cd notebooks
jupyter notebook example_mlflow.ipynb
```

### 3. Verificar os Containers
```bash
# No terminal do VS Code:
docker compose ps
```

### 4. Ver logs do MLflow
```bash
docker logs -f mlops-mlflow-server-1
```

## 🔄 Comandos Úteis

### Reiniciar MLflow
```bash
docker restart mlops-mlflow-server-1
```

### Parar todos os serviços
```bash
docker compose down
```

### Iniciar todos os serviços
```bash
docker compose up -d
```

### Ver status
```bash
docker compose ps
```

## 💡 Dicas Importantes

### ✅ O QUE FUNCIONA:
- Editar código no VS Code local → Salvo no Codespace
- Acessar `localhost:5000` → Redireciona para MLflow no Codespace
- Terminal do VS Code → Executa comandos NO Codespace
- Git commits/push → Funciona normalmente
- Extensões do VS Code → Funcionam no ambiente remoto

### ⚠️ IMPORTANTE SABER:
- Os arquivos estão NO Codespace (não no seu PC)
- Docker roda NO Codespace (não consome recursos locais)
- Para economizar: Pare o Codespace quando não usar
- Port forwarding é automático (não precisa configurar)

## 🛑 Ao Terminar de Usar

### 1. Parar os containers
```bash
docker compose down
```

### 2. Desconectar VS Code
```
Canto inferior esquerdo → > Codespaces → Close Remote Connection
```

### 3. Parar o Codespace no GitHub
```
GitHub → Codespaces → [...] → Stop codespace
```

## 🐛 Troubleshooting

### Porta não funciona?
1. Abra o painel **PORTS** no VS Code
2. Verifique se a porta está "Forwarded"
3. Se não: Clique direito → "Forward Port" → Digite a porta

### MLflow não responde?
```bash
# Reinicie o container:
docker restart mlops-mlflow-server-1

# Aguarde 10 segundos e teste:
curl http://localhost:5000
```

### Codespace lento?
```bash
# Limpe containers antigos:
docker system prune -a

# Reinicie os serviços:
docker compose down && docker compose up -d
```

## 📚 Links Úteis

- **README Completo**: [README.md](./README.md)
- **Documentação MLflow**: https://mlflow.org/docs/latest/
- **GitHub Codespaces**: https://github.com/features/codespaces
- **VS Code Remote**: https://code.visualstudio.com/docs/remote/codespaces

---

## 🎓 Próximos Passos

1. ✅ Abra o notebook: `notebooks/example_mlflow.ipynb`
2. ✅ Execute as células e veja os experimentos no MLflow
3. ✅ Explore o MinIO Console: http://localhost:9001 (user/password)
4. ✅ Crie seus próprios experimentos!

**Dúvidas?** Consulte o [README.md](./README.md) completo com todas as opções e detalhes.
