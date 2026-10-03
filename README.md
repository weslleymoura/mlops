
# Projeto MLOps com MLFlow

> **Atenção usuários Windows:**
>
> Antes de seguir as instruções abaixo, recomenda-se configurar o WSL (Windows Subsystem for Linux) para garantir compatibilidade total com Docker, Conda e comandos Linux. Siga o guia:
>
> [Guia de instalação e uso do WSL](docs/WSL.md)

## Pré-requisitos

1. Conta no GitHub (gratuita)
2. VS Code instalado ([baixar](https://code.visualstudio.com/))
3. Anaconda ou Miniconda instalado ([baixar](https://docs.conda.io/en/latest/miniconda.html))
4. Git instalado
5. Docker Desktop ([baixar](https://www.docker.com/products/docker-desktop/))

## Fazer Fork e Clonar o Repositório

1. No GitHub, acesse: https://github.com/weslleymoura/mlops
2. Clique em **Fork**
3. Depois, clone seu fork:
   ```bash
   git clone https://github.com/SEU-USUARIO/mlops.git
   cd mlops
   ```

## Criar e Ativar o Ambiente Conda

1. Crie o ambiente:
   ```bash
   conda create -n mlops-util-env --override-channels -c conda-forge python=3.11
   ```
2. Ative o ambiente:
   ```bash
   conda activate mlops-util-env
   ```
3. Instale as dependências:
   ```bash
   conda install --override-channels -c conda-forge --file requirements/requirements_conda.txt
   ```

> **Erro `CondaToSNonInteractiveError` (Terms of Service)?** Confira se os comandos acima incluem `--override-channels -c conda-forge`. Essa opção faz o conda usar somente o canal conda-forge, que não exige aceitar termos de uso.

### Abrir o Jupyter Lab

1. Ative o seu ambiente conda
   ```bash
   conda activate mlops-util-env
   ```
2. Abra o Jupyter Lab:
   ```bash
   jupyter lab
   ```
3. Abra os notebooks na pasta `notebooks/`.

## Subir os Serviços Docker

1. Crie o arquivo `.env` a partir do exemplo (sem ele, os notebooks não se conectam ao MLflow):
   ```bash
   cp .env.example .env
   ```
2. No diretório do projeto, execute:
   ```bash
   docker compose up
   ```
3. Os serviços MLflow, CloudServer (S3) e Postgres serão iniciados.

### Testar o Ambiente

Para verificar se está tudo funcionando (Docker, portas, serviços e registro no MLflow), ative o ambiente conda e rode:
```bash
bash scripts/testar-ambiente.sh
```

### Acessar os Serviços

- MLflow UI: http://localhost:5010
- CloudServer (S3): http://localhost:9000 (access key: `user`, secret: `password`)
- Postgres: localhost:5433 (user: `user`, senha: `password`)

## Dicas

- Use VS Code para editar os scripts do projeto.
- Use o ambiente Conda para rodar notebooks e scripts Python.
- Pare os serviços Docker com:
  ```bash
  docker compose down
  ```
- [Arquivo de referência (comandos úteis)](docs/REFERENCE.md)

Pronto! Agora você pode trabalhar localmente com MLflow, CloudServer (S3), Postgres e Jupyter Lab.

---
