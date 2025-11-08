# MLflow Lab — Template para GitHub Codespaces

Este repositório prepara um ambiente de estudo com **MinIO + Postgres + MLflow** dentro de um Codespace GitHub ou ambiente local.

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

# Desativar ambiente virtual
deactivate
```

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

---

## 🐛 Troubleshooting

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