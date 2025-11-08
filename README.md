# MLflow Lab — Template para GitHub Codespaces

Este repositório prepara um ambiente de estudo com **MinIO + Postgres + MLflow** dentro de um Codespace GitHub ou ambiente local.

## 🎯 Formas de usar este projeto

| Opção | Descrição | Onde roda | Ideal para |
|-------|-----------|-----------|------------|
| **Opção 1** | Codespace completo (navegador) | Tudo na nuvem | Testes rápidos, sem instalação local |
| **Opção 2** | Codespace + Desenvolvimento local | Serviços na nuvem, código local | Economizar recursos locais |
| **Opção 3** | VS Code local conectado ao Codespace | Serviços na nuvem, interface local | Melhor experiência de desenvolvimento |
| **Local** | Instalação completa no computador | Tudo local | Offline, controle total |

➡️ **Recomendado**: Use a **Opção 3** (VS Code local + Codespace) para melhor experiência!

📖 **Documentação adicional:**
- **[Guia Rápido de Setup](./QUICKSTART.md)** - Tutorial passo a passo em 3 minutos
- **[Checklist Completo](./CHECKLIST.md)** - Verificação passo a passo para garantir que tudo funciona
- **[Referência Rápida](./REFERENCE.md)** - Todos os comandos essenciais em um só lugar

## O que está incluso
- `docker-compose.yml` com MinIO, 2x Postgres, MLflow Server e um client.
- `.devcontainer/devcontainer.json` para iniciar o Codespace e executar `docker compose up -d` automaticamente.
- `Dockerfile` base (Python 3.13) usado para `mlflow-server` e `client`.
- `notebooks/example_mlflow.ipynb` — notebook de exemplo que registra um experimento no MLflow.
- `requirements.txt` — dependências Python do projeto.

---

## 🚀 Como usar no GitHub Codespaces 

### Opção 1: Trabalhar dentro do Codespace (ambiente completo)

1. Faça fork ou clone deste repositório para sua conta/organização.
2. Abra **Code → Codespaces → Create codespace on main**.
3. O devcontainer executará automaticamente:
   - Criação do ambiente virtual Python (`mlops-util-env`)
   - Instalação das dependências do `requirements.txt`
   - Inicialização dos containers Docker
4. Para visualizar:
   - **MinIO Console**: porta `9001` (usuário: `user`, senha: `password`)
   - **MLflow UI**: porta `5000`
   - **Postgres (MLflow)**: porta `5433`
   - **Postgres (MLOps)**: porta `5434`
5. Para parar o ambiente: `docker compose down`

### Opção 2: Codespace como servidor + Desenvolvimento local 🌟

Use o Codespace **apenas para rodar os serviços** e desenvolva no seu computador local:

#### No Codespace:
1. Crie o Codespace normalmente
2. Os containers serão iniciados automaticamente
3. As portas são automaticamente encaminhadas para seu `localhost`

#### No seu computador local:
1. **Não precisa instalar Docker!** Os serviços rodam no Codespace
2. Configure seu ambiente Python local:
   ```bash
   python -m venv mlops-util-env
   source mlops-util-env/bin/activate  # Windows: mlops-util-env\Scripts\activate
   pip install -r requirements.txt
   ```
3. Acesse os serviços via `localhost`:
   - **MLflow UI**: http://localhost:5000
   - **MinIO Console**: http://localhost:9001
   - Seus notebooks e scripts Python se conectam em `http://localhost:5000`

#### Vantagens:
- ✅ Não consome recursos locais (Docker roda na nuvem)
- ✅ Mesma experiência de desenvolvimento
- ✅ Código e dados no seu computador
- ✅ Serviços sempre disponíveis enquanto o Codespace estiver ativo

#### Como funciona:
O VS Code cria automaticamente túneis SSH para as portas do Codespace. Você verá no painel **PORTS** (canto inferior) as portas encaminhadas. Basta acessar `localhost:porta` normalmente!

### Opção 3: Conectar VS Code Local ao Codespace 🔗

Você pode usar o VS Code instalado no seu computador para se conectar ao Codespace, tendo acesso total ao ambiente remoto:

#### Pré-requisitos:
- **VS Code** instalado localmente ([download aqui](https://code.visualstudio.com/))
- Extensão **GitHub Codespaces** instalada no VS Code
  - Abra o VS Code → Extensions (Ctrl+Shift+X) → Procure por "GitHub Codespaces" → Instale

#### Passo a passo:

1. **Crie o Codespace** (se ainda não criou):
   - No GitHub, abra este repositório
   - Clique em **Code** → **Codespaces** → **Create codespace on main**
   - Aguarde a criação do Codespace

2. **Conecte o VS Code local ao Codespace**:
   
   **Método 1: Pela interface do VS Code**
   - Abra o VS Code no seu computador
   - Pressione `Ctrl+Shift+P` (ou `Cmd+Shift+P` no Mac)
   - Digite: `Codespaces: Connect to Codespace`
   - Selecione o Codespace criado da lista

   **Método 2: Pelo GitHub**
   - No GitHub, vá em **Code** → **Codespaces**
   - Clique nos **três pontos (...)** ao lado do Codespace ativo
   - Selecione **Open in Visual Studio Code**
   - O VS Code local será aberto automaticamente conectado ao Codespace

3. **Verifique a conexão**:
   - No canto inferior esquerdo do VS Code, você verá: **> Codespaces: nome-do-codespace**
   - Todas as operações agora acontecem no ambiente remoto

4. **Acesse os serviços**:
   - Vá para a aba **PORTS** no painel inferior do VS Code
   - As portas do Codespace estarão automaticamente encaminhadas:
     - `5000` → MLflow UI
     - `9000` → MinIO API
     - `9001` → MinIO Console
     - `5433` → Postgres (MLflow)
     - `5434` → Postgres (MLOps)
   - Clique em **Open in Browser** ou acesse via `http://localhost:porta`

#### Vantagens desta abordagem:
- ✅ **Interface nativa** do VS Code (mais rápido que o navegador)
- ✅ **Extensões locais** funcionam no ambiente remoto
- ✅ **Git integrado** com suas credenciais locais
- ✅ **Terminal remoto** diretamente no VS Code
- ✅ **Port forwarding automático** para todos os serviços
- ✅ **Sincronização de configurações** (settings, keybindings, snippets)

#### Desenvolvimento híbrido:
Você pode trabalhar tanto no Codespace quanto localmente:
- **Arquivos e código**: Editados remotamente (no Codespace)
- **Serviços Docker**: Rodam remotamente (no Codespace)
- **Interface**: VS Code local (seu computador)
- **Acesso às portas**: Via `localhost` (encaminhamento automático)

#### Dicas importantes:
- 💡 O terminal do VS Code executa comandos **dentro do Codespace**
- 💡 Você pode abrir múltiplas janelas do VS Code conectadas ao mesmo Codespace
- 💡 Para desconectar: Feche o VS Code ou clique em **> Codespaces** (canto inferior esquerdo) → **Close Remote Connection**
- 💡 O Codespace continua rodando mesmo após desconectar (pare-o no GitHub para economizar créditos)

---

## 💻 Configuração do Ambiente Local

### Pré-requisitos
- Python 3.13 ou superior
- Docker e Docker Compose
- Git

### Passo a passo

#### 1. Clone o repositório
```bash
git clone https://github.com/weslleymoura/mlops.git
cd mlops
```

#### 2. Crie e ative o ambiente virtual Python
```bash
# Criar ambiente virtual
python -m venv mlops-util-env

# Ativar ambiente (macOS/Linux)
source mlops-util-env/bin/activate

# Ativar ambiente (Windows)
mlops-util-env\Scripts\activate
```

#### 3. Instale as dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Inicie os containers Docker
```bash
docker compose up -d
```

#### 5. Verifique se os serviços estão rodando
```bash
docker compose ps
```

#### 6. Acesse as interfaces

- **MLflow UI**: http://localhost:5000
- **MinIO Console**: http://localhost:9001
  - Usuário: `user`
  - Senha: `password`

#### 7. Execute o notebook de exemplo
```bash
jupyter notebook notebooks/example_mlflow.ipynb
```

### Comandos úteis

```bash
# Ver logs dos containers
docker compose logs -f

# Parar os containers
docker compose down

# Parar e remover volumes (limpa dados)
docker compose down -v

# Reconstruir as imagens
docker compose up -d --build

# Reiniciar apenas o MLflow
docker restart mlops-mlflow-server-1

# Ver status dos containers
docker compose ps

# Desativar ambiente virtual
deactivate
```

### Gerenciamento do Codespace

```bash
# Ver status dos containers no Codespace
docker compose ps

# Parar serviços (economiza créditos)
docker compose down

# Reiniciar serviços
docker compose up -d

# Ver uso de recursos
docker stats

# Limpar espaço em disco
docker system prune -a
```

**Parar/Iniciar Codespace pelo GitHub:**
- Acesse: https://github.com/codespaces
- Clique nos **três pontos (...)** ao lado do Codespace
- Selecione **Stop codespace** ou **Delete** quando não estiver usando

**Comandos VS Code para Codespaces:**
- `Ctrl+Shift+P` → `Codespaces: Stop Current Codespace` - Para o Codespace
- `Ctrl+Shift+P` → `Codespaces: Disconnect` - Desconecta mas mantém rodando
- `Ctrl+Shift+P` → `Codespaces: Delete Codespace` - Remove o Codespace

---

## 📦 Estrutura do Projeto

```
mlops/
├── .devcontainer/
│   └── devcontainer.json      # Configuração do GitHub Codespaces
├── notebooks/
│   └── example_mlflow.ipynb   # Notebook de exemplo
├── docker-compose.yml          # Orquestração dos serviços
├── Dockerfile                  # Imagem base Python
├── requirements.txt            # Dependências Python
├── .gitignore                  # Arquivos ignorados pelo Git
└── README.md                   # Este arquivo
```

---

## 🔧 Serviços Disponíveis

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| MinIO | 9000, 9001 | Object Storage (S3-compatible) |
| MLflow Server | 5000 | UI e API do MLflow |
| Postgres (MLflow) | 5433 | Backend store do MLflow |
| Postgres (MLOps) | 5434 | Banco de dados auxiliar |
| Client | - | Container para execução de scripts |

---

## 🎓 Dicas

- **GitHub Codespaces**: Desliguem o Compose (`docker compose down`) ao terminar para economizar horas.
- **Port Forwarding**: Quando conectado ao Codespace via VS Code desktop, as portas são automaticamente encaminhadas para localhost.
- **Ambiente Local**: Sempre ative o ambiente virtual antes de trabalhar no projeto.
- **Jupyter**: O notebook já está configurado para se conectar ao MLflow em `http://localhost:5000`.
- **Versionamento**: O ambiente virtual (`mlops-util-env/`) não é versionado no Git.
- **Modo híbrido**: Você pode trabalhar no Codespace e depois mudar para local (ou vice-versa) sem problemas!

### 🔄 Fluxo de trabalho recomendado com Codespace + VS Code Local

```
┌─────────────────────────────────────────────────────────────┐
│  Seu Computador Local (VS Code)                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • Interface do VS Code                              │  │
│  │  • Edição de código                                  │  │
│  │  • Git (commits, push, pull)                         │  │
│  │  • Extensões e ferramentas                           │  │
│  └──────────────────────────────────────────────────────┘  │
│                           │                                 │
│                           │ SSH Tunnel (automático)         │
│                           ▼                                 │
└─────────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────┐
│  GitHub Codespace (Nuvem) │                                 │
│  ┌────────────────────────▼──────────────────────────────┐  │
│  │  Container Dev (Python + Docker)                      │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │ Docker Compose (Serviços)                       │  │  │
│  │  │  • MLflow Server      → localhost:5000          │  │  │
│  │  │  • MinIO Console      → localhost:9001          │  │  │
│  │  │  • Postgres (MLflow)  → localhost:5433          │  │  │
│  │  │  • Postgres (MLOps)   → localhost:5434          │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

**Como usar:**
1. Conecte o VS Code local ao Codespace
2. Edite arquivos normalmente (salvos no Codespace)
3. Acesse serviços via `localhost:porta` no navegador local
4. Execute comandos no terminal (rodam no Codespace)
5. Ao terminar: `docker compose down` e pare o Codespace no GitHub

---

## 🐛 Troubleshooting

### Não consigo acessar os serviços no localhost

**Se estiver usando Codespace conectado ao VS Code local:**

1. Verifique o painel **PORTS** no VS Code (View → Ports ou Ctrl+\`):
   - As portas devem estar listadas com status "Forwarded"
   - Se não estiver visível, clique com botão direito na porta → "Forward Port"

2. Verifique se os containers estão rodando no Codespace:
   ```bash
   docker compose ps
   ```

3. Se a porta não encaminhar automaticamente:
   - Abra o painel **PORTS**
   - Clique em **Forward a Port**
   - Digite a porta (exemplo: `5000`)
   - Acesse `http://localhost:5000`

4. Problemas de visibilidade:
   - Clique com botão direito na porta no painel PORTS
   - Verifique se está marcado como **Public** ou **Private**
   - Para MLflow, MinIO e Postgres, **Private** é suficiente

### Erro de conexão com o MLflow
Certifique-se de que os containers estão rodando:
```bash
docker compose ps
```

### Porta já em uso
Se alguma porta estiver em uso, edite o `docker-compose.yml` e altere o mapeamento de portas.

### Problemas com dependências Python
Recrie o ambiente virtual:
```bash
deactivate
rm -rf mlops-util-env
python -m venv mlops-util-env
source mlops-util-env/bin/activate  # ou mlops-util-env\Scripts\activate no Windows
pip install -r requirements.txt
```

---

## 📝 Licença

Este projeto é um template educacional para estudo de MLOps com MLflow.