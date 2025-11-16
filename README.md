# MLflow Lab — Ambiente Híbrido para MLOps

Este repositório prepara um ambiente de estudo com **MinIO + Postgres + MLflow** usando uma arquitetura híbrida: **serviços na nuvem (Codespace)** + **desenvolvimento local (seu computador)**.

## 🎯 Como funciona

Você vai trabalhar com **dois VS Codes ao mesmo tempo**:

```
┌─────────────────────────────────────┐
│  VS Code #1 - Codespace             │
│  • Conectado ao GitHub Codespace    │
│  • Serviços Docker rodando          │
│  • MLflow, MinIO, Postgres          │
│  • Apenas para manter serviços UP   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│  VS Code #2 - Local                 │
│  • Seu projeto no computador        │
│  • Ambiente Conda Python 3.13       │
│  • Notebooks e código               │
│  • Acessa serviços via localhost    │
└─────────────────────────────────────┘

        Port Forwarding Automático
        localhost:5000 → Codespace
        localhost:9001 → Codespace
```

## ✅ Vantagens desta arquitetura

- ✅ **Não precisa Docker local** - Roda no Codespace
- ✅ **Desenvolvimento no seu PC** - Mais rápido e familiar
- ✅ **Acesso via localhost** - Transparente via port forwarding
- ✅ **Notebooks no seu computador** - Commit direto para seu fork
- ✅ **Economia de recursos** - Codespace só para serviços

---

## 🚀 Setup Inicial (15 minutos)

### Pré-requisitos

1. **Conta no GitHub** (gratuita)
2. **VS Code** instalado ([baixar](https://code.visualstudio.com/))
3. **Extensão GitHub Codespaces** no VS Code
4. **Anaconda/Miniconda** instalado ([baixar](https://docs.conda.io/en/latest/miniconda.html))
5. **Git** instalado

---

## 📋 Parte 1: Fork e Codespace (Serviços)

### 1. Fazer Fork do repositório

1. No GitHub, acesse: https://github.com/weslleymoura/mlops
2. Clique em **Fork** (canto superior direito)
3. Aguarde a criação do fork na sua conta

### 2. Criar Codespace (serviços na nuvem)

No **seu fork** do GitHub:

1. Clique em **Code** → **Codespaces**
2. Clique em **Create codespace on main**
3. Aguarde 2-3 minutos (instalação automática)

✅ O Codespace vai inicializar automaticamente:
- Python 3.13 + ambiente virtual
- Docker Compose com MLflow, MinIO e Postgres

### 3. Conectar VS Code #1 ao Codespace

1. Abra o VS Code no seu computador
2. Pressione `Ctrl+Shift+P` (ou `Cmd+Shift+P` no Mac)
3. Digite: `Codespaces: Connect to Codespace`
4. Selecione seu Codespace

### 4. Verificar serviços no Codespace

No VS Code conectado ao Codespace:

```bash
# Ver status dos containers
docker compose ps

# Todos devem estar "Up" ✅
```

**Se o MLflow não subir:**

```bash
docker compose restart mlflow-server
docker compose logs mlflow-server
```

### 5. Testar acesso aos serviços

No seu **navegador local**:
- MLflow: http://localhost:5000
- MinIO Console: http://localhost:9001 (user: `user`, senha: `password`)

✅ **Pronto!** Deixe este VS Code aberto (conectado ao Codespace).

---

## 💻 Parte 2: Ambiente Local (Desenvolvimento)

### 1. Clonar seu fork localmente

```bash
# Substituir SEU-USUARIO pelo seu usuário do GitHub
git clone https://github.com/SEU-USUARIO/mlops.git
cd mlops
```

### 2. Configurar ambiente Conda

```bash
# Criar ambiente com Python 3.13
conda create -n mlops-util-env python=3.11

# Ativar ambiente
conda activate mlops-util-env

# Instalar dependências
conda install -c conda-forge --file requirements/requirements_conda.txt

# Registrar kernel Jupyter
python -m ipykernel install --user --name mlops-util-env
```

### 3. Abrir VS Code #2 (Local)

```bash
# No diretório do projeto
code .
```

Ou abra o VS Code e: **File → Open Folder** → Selecione a pasta `mlops`

---

## 🔄 Fluxo de Trabalho Diário

### Iniciar trabalho

1. **VS Code #1 (Codespace)**:
   - Conectar ao Codespace
   - Verificar: `docker compose ps`
   - Deixar aberto em segundo plano

2. **VS Code #2 (Local)**:
   - Ativar ambiente: `conda activate mlops-util-env`
   - Abrir projeto: `code .`
   - Trabalhar normalmente nos notebooks/código

3. **Navegador**:
   - MLflow UI: http://localhost:5000
   - MinIO Console: http://localhost:9001

### Finalizar trabalho

1. **No VS Code Local (seu projeto)**:
   ```bash
   git add .
   git commit -m "Descrição das alterações"
   git push origin main
   ```

2. **No VS Code do Codespace**:
   ```bash
   docker compose down
   ```

3. **No GitHub**:
   - Vá em https://github.com/codespaces
   - Clique em `[...]` → **Stop codespace**

⚠️ **Importante:** Sempre pare o Codespace quando terminar!

---

## 📊 Acessar serviços

| Serviço | URL | Credenciais |
|---------|-----|-------------|
| **MLflow UI** | http://localhost:5000 | - |
| **MinIO Console** | http://localhost:9001 | user / password |
| **Postgres (MLflow)** | localhost:5433 | user / password |
| **Postgres (MLOps)** | localhost:5434 | mlops_user / admin |

---

## 🐛 Troubleshooting

### MLflow não abre (localhost:5000)

```bash
# No VS Code do Codespace
docker compose restart mlflow-server
docker compose logs mlflow-server
```

### Portas não funcionam

1. No VS Code conectado ao Codespace, abra o painel **PORTS**
2. Verifique se as portas estão "Forwarded"
3. Se não: Clique direito → "Forward Port" → Digite a porta (5000, 9001, etc)

### Conda não encontra pacotes

```bash
# Tente com diferentes canais
conda install -c conda-forge -c anaconda --file requirements/requirements_conda.txt
```

### Kernel do Jupyter não aparece

```bash
conda activate mlops-util-env
python -m ipykernel install --user --name mlops-util-env --display-name "Python 3.13 (mlops-util-env)"
jupyter kernelspec list
```

---

## 💡 Dicas

- ✅ **VS Code #1** (Codespace): Apenas para manter serviços rodando
- ✅ **VS Code #2** (Local): Para desenvolvimento (notebooks, código)
- ✅ O Codespace consome créditos gratuitos do GitHub (60h/mês)
- ✅ Sempre pare o Codespace quando não estiver usando
- ✅ Port forwarding é automático quando conectado ao Codespace
- ✅ Seus arquivos ficam no seu fork do GitHub

---

## 📚 Documentação Adicional

- **[Guia Rápido](./docs/QUICKSTART.md)** - Setup em 5 passos
- **[Checklist](./docs/CHECKLIST.md)** - Verificação completa
- **[Referência](./docs/REFERENCE.md)** - Comandos essenciais

---

## 📝 Licença

Este projeto é um template educacional para estudo de MLOps com MLflow.
