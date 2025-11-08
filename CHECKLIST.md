# ✅ Checklist de Configuração

Use este checklist para garantir que tudo está funcionando corretamente.

---

## 📋 Antes de Começar

- [ ] Tenho uma conta no GitHub
- [ ] VS Code está instalado no meu computador
- [ ] Extensão "GitHub Codespaces" está instalada no VS Code

---

## 🚀 Passo 1: Criar o Codespace

- [ ] Abri o repositório no GitHub
- [ ] Cliquei em **Code** → **Codespaces** → **Create codespace on main**
- [ ] Aguardei a criação (2-3 minutos)
- [ ] Vi a mensagem de sucesso

---

## 🔌 Passo 2: Conectar VS Code Local

- [ ] Abri o VS Code no meu computador
- [ ] Pressionei `Ctrl+Shift+P` (ou usei GitHub → [...] → Open in VS Code)
- [ ] Digitei: "Codespaces: Connect to Codespace"
- [ ] Selecionei o Codespace da lista
- [ ] Aguardei a conexão

---

## ✔️ Passo 3: Verificar Conexão

- [ ] No canto inferior esquerdo vejo: **> Codespaces: [nome]**
- [ ] Abri o terminal (`` Ctrl+` ``)
- [ ] O terminal mostra o prompt do Codespace
- [ ] Executei `docker compose ps` e vi os containers

---

## 🌐 Passo 4: Verificar Serviços

### MLflow
- [ ] Abri http://localhost:5000 no navegador
- [ ] Vejo a interface do MLflow
- [ ] Vejo o experimento "Default"

### MinIO
- [ ] Abri http://localhost:9001 no navegador
- [ ] Fiz login com: `user` / `password`
- [ ] Vejo o bucket "bucket" criado

### Containers
- [ ] No terminal: `docker compose ps`
- [ ] Todos os containers estão "Up":
  - [ ] mlops-minio-1
  - [ ] mlops-postgres-1
  - [ ] mlops-mlflow-server-1
  - [ ] mlops-client-1

---

## 📓 Passo 5: Testar Notebook

- [ ] Abri `notebooks/example_mlflow.ipynb`
- [ ] Selecionei o kernel Python (mlops-util-env)
- [ ] Executei todas as células (Run All)
- [ ] Vi o experimento aparecer no MLflow UI

---

## 🎉 Verificação Final

### Tudo funcionando se:
- [ ] VS Code está conectado ao Codespace
- [ ] MLflow UI abre em localhost:5000
- [ ] Containers estão rodando
- [ ] Notebook executa sem erros
- [ ] Experimentos aparecem no MLflow

---

## 🐛 Problemas?

### MLflow não abre (localhost:5000)
```bash
docker restart mlops-mlflow-server-1
# Aguarde 10 segundos
```

### Porta não funciona
```
VS Code → View → Ports → Clique direito → Forward Port → Digite 5000
```

### Containers não rodando
```bash
docker compose ps
docker compose up -d
```

---

## 💡 Lembrar

- ✅ Terminal do VS Code roda no Codespace
- ✅ Arquivos estão no Codespace (faça commits!)
- ✅ Sempre execute `docker compose down` ao terminar
- ✅ Pare o Codespace no GitHub quando não usar

---

📚 **Documentação**: [README.md](./README.md) | [QUICKSTART.md](./QUICKSTART.md) | [REFERENCE.md](./REFERENCE.md)
