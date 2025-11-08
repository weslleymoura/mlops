# 🚀 Guia Rápido: Setup em 5 minutos

## ✅ Pré-requisitos (Instalar uma vez)

1. **VS Code** instalado → [Download](https://code.visualstudio.com/)
2. **Extensão GitHub Codespaces** no VS Code:
   - Abra o VS Code
   - Pressione `Ctrl+Shift+X`
   - Procure: "GitHub Codespaces"
   - Clique em "Install"

---

## 🎯 Setup em 3 Passos

### 1️⃣ Criar o Codespace (2 minutos)

No GitHub, neste repositório:

```
Code → Codespaces → Create codespace on main
```

Aguarde 2-3 minutos. O Codespace vai configurar tudo automaticamente.

---

### 2️⃣ Conectar VS Code Local (1 minuto)

**Opção A: Pelo GitHub** (mais rápido)
```
GitHub → Codespaces → [...] → Open in Visual Studio Code
```

**Opção B: Pelo VS Code**
```
Ctrl+Shift+P → "Codespaces: Connect to Codespace" → Selecione o codespace
```

---

### 3️⃣ Testar (30 segundos)

1. **Verifique a conexão:**
   - Canto inferior esquerdo do VS Code: **> Codespaces: [nome]** ✅

2. **Abra o MLflow:**
   - Navegador: http://localhost:5000 ✅

3. **Verifique os containers:**
   - Terminal do VS Code: `docker compose ps` ✅

---

## 🎉 Pronto! Agora você pode:

### 📓 Executar o notebook
```
No VS Code: notebooks/example_mlflow.ipynb → Run All
```

### 🌐 Acessar os serviços

| Serviço | URL | Login |
|---------|-----|-------|
| MLflow UI | http://localhost:5000 | - |
| MinIO Console | http://localhost:9001 | user / password |

### 🐳 Comandos Docker úteis

```bash
# Ver status
docker compose ps

# Ver logs do MLflow
docker logs -f mlops-mlflow-server-1

# Reiniciar MLflow
docker restart mlops-mlflow-server-1
```

---

## 🛑 Ao Terminar

```bash
# 1. Parar serviços no terminal do VS Code
docker compose down

# 2. Fechar VS Code (ou desconectar: Ctrl+Shift+P → Close Remote Connection)

# 3. Parar o Codespace no GitHub
https://github.com/codespaces → [...] → Stop codespace
```

**� Importante:** Sempre pare o Codespace para economizar créditos!

---

## 🐛 Problemas?

### MLflow não abre
```bash
docker restart mlops-mlflow-server-1
# Aguarde 10 segundos e acesse novamente
```

### Porta não funciona
```
VS Code → Painel PORTS (View → Ports) → Clique direito → Forward Port → Digite 5000
```

### Codespace não conecta
```
Feche o VS Code → Abra novamente → Tente conectar de novo
```

---

📚 **Documentação completa**: [README.md](./README.md)
✅ **Checklist detalhado**: [CHECKLIST.md](./CHECKLIST.md)
📌 **Referência de comandos**: [REFERENCE.md](./REFERENCE.md)
