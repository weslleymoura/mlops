# MLflow Lab — Template para GitHub Codespaces

Este repositório prepara um ambiente de estudo completo com **MinIO + Postgres + MLflow** usando GitHub Codespaces e VS Code local.

## 🎯 Como funciona

Você vai usar o **VS Code instalado no seu computador** conectado a um **GitHub Codespace** onde os serviços rodam:

```
┌─────────────────────────────────────┐
│  Seu Computador                     │
│  • VS Code (interface)              │
│  • Navegador (acessar serviços)     │
└─────────────┬───────────────────────┘
              │ Conexão automática
┌─────────────▼───────────────────────┐
│  GitHub Codespace (Nuvem)           │
│  • MLflow Server (localhost:5000)   │
│  • MinIO (localhost:9001)           │
│  • Postgres                         │
│  • Seus arquivos e código           │
└─────────────────────────────────────┘
```

**Vantagens:**
- ✅ Não precisa instalar Docker no seu computador
- ✅ Interface nativa do VS Code (mais rápida que o navegador)
- ✅ Acesso aos serviços via `localhost` (port forwarding automático)
- ✅ Seus arquivos ficam seguros no GitHub

## O que está incluso
- `docker-compose.yml` — MinIO, Postgres e MLflow Server
- `.devcontainer/` — Configuração automática do Codespace
- `notebooks/example_mlflow.ipynb` — Notebook de exemplo
- `requirements.txt` — Dependências Python

---

## 🚀 Como começar (5 minutos)

### Pré-requisitos

#### Pré-requisitos

1. **VS Code** instalado no seu computador ([baixar aqui](https://code.visualstudio.com/))
2. **Extensão GitHub Codespaces** no VS Code:
   - Abra o VS Code
   - Pressione `Ctrl+Shift+X` (Extensions)
   - Procure por "GitHub Codespaces"
   - Clique em "Install"

### Passo a passo

#### 1️⃣ Criar o Codespace (2 minutos)

No GitHub, neste repositório:
1. Clique em **Code** → **Codespaces**
2. Clique em **Create codespace on main**
3. Aguarde a criação (2-3 minutos)

O Codespace vai iniciar automaticamente:
- ✅ Python 3.13 + ambiente virtual
- ✅ Docker Compose com todos os serviços
- ✅ MLflow, MinIO e Postgres

#### 2️⃣ Conectar VS Code Local (1 minuto)

**Opção A: Pelo VS Code**
1. Abra o VS Code no seu computador
2. Pressione `Ctrl+Shift+P` (ou `Cmd+Shift+P` no Mac)
3. Digite: `Codespaces: Connect to Codespace`
4. Selecione o Codespace da lista

**Opção B: Pelo GitHub** (mais rápido)
1. No GitHub, clique em **Code** → **Codespaces**
2. Clique nos **três pontos (...)** ao lado do Codespace
3. Selecione **Open in Visual Studio Code**

#### 3️⃣ Verificar que tudo está funcionando (30 segundos)

No VS Code conectado ao Codespace:

1. **Verifique a conexão**: 
   - Canto inferior esquerdo: **> Codespaces: [nome]** ✅

2. **Verifique as portas**:
   - Abra o painel **PORTS** (View → Ports)
   - Você deve ver as portas encaminhadas:

| Porta | Serviço | URL Local |
|-------|---------|-----------|
| 5000 | MLflow UI | http://localhost:5000 |
| 9001 | MinIO Console | http://localhost:9001 |
| 5433 | Postgres (MLflow) | localhost:5433 |

3. **Teste o MLflow**:
   - Abra seu navegador: http://localhost:5000
   - Você deve ver a interface do MLflow ✅

4. **Verifique os containers**:
   - Abra o terminal no VS Code (`` Ctrl+` ``)
   - Execute: `docker compose ps`
   - Todos devem estar "Up" ✅

---

## � Usando o ambiente

### Executar o notebook de exemplo

1. No VS Code, abra: `notebooks/example_mlflow.ipynb`
2. Selecione o kernel Python (mlops-util-env)
3. Execute as células (`Run All` ou `Shift+Enter`)
4. Veja os experimentos aparecerem no MLflow: http://localhost:5000

### Acessar os serviços

| Serviço | URL | Credenciais |
|---------|-----|-------------|
| **MLflow UI** | http://localhost:5000 | - |
| **MinIO Console** | http://localhost:9001 | user / password |

### Comandos úteis do Docker

Execute no terminal do VS Code (conectado ao Codespace):

```bash
# Ver status dos containers
docker compose ps

# Ver logs do MLflow
docker logs -f mlops-mlflow-server-1

# Reiniciar o MLflow
docker restart mlops-mlflow-server-1

# Parar todos os serviços
docker compose down

# Iniciar todos os serviços
docker compose up -d
```

### Gerenciar o Codespace

**Ao terminar de usar:**

1. No terminal do VS Code: `docker compose down`
2. Desconectar: Feche o VS Code ou `Ctrl+Shift+P` → `Close Remote Connection`
3. No GitHub: https://github.com/codespaces → `[...]` → **Stop codespace**

**Importante:** Sempre pare o Codespace quando não estiver usando para economizar créditos do GitHub!



---

## 🐛 Troubleshooting

### MLflow não abre (localhost:5000)

```bash
# Reinicie o container
docker restart mlops-mlflow-server-1

# Aguarde 10 segundos e teste
curl http://localhost:5000/health
```

### Portas não funcionam

1. Abra o painel **PORTS** no VS Code (View → Ports)
2. Verifique se as portas estão "Forwarded"
3. Se não: Clique direito → "Forward Port" → Digite a porta (5000, 9001, etc)

### Containers não estão rodando

```bash
# Verificar status
docker compose ps

# Se estiverem parados, iniciar
docker compose up -d

# Ver logs se houver erros
docker compose logs
```

### Codespace lento ou travando

```bash
# Limpar cache do Docker
docker system prune -a

# Reiniciar serviços
docker compose down && docker compose up -d
```

---

## � Dicas importantes

- ✅ O terminal do VS Code executa comandos **no Codespace** (não no seu PC)
- ✅ Os arquivos estão **no Codespace** (faça commits para não perder)
- ✅ Port forwarding é **automático** (localhost funciona direto)
- ✅ Sempre execute `docker compose down` antes de parar o Codespace
- ✅ Pare o Codespace no GitHub quando não estiver usando (economiza créditos)

---

## 📚 Documentação Adicional

- **[Guia Rápido](./QUICKSTART.md)** - Setup em 3 passos (5 minutos)
- **[Checklist](./CHECKLIST.md)** - Verificação completa passo a passo
- **[Referência](./REFERENCE.md)** - Comandos essenciais

---

## �📝 Licença

Este projeto é um template educacional para estudo de MLOps com MLflow.