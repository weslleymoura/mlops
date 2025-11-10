# ✅ Checklist Completo — Ambiente Híbrido MLOps

Use este checklist para verificar se tudo está configurado corretamente.

---

## 📋 Parte 1: Codespace (Serviços)

### Fork e Codespace

- [ ] Fork do repositório criado na minha conta do GitHub
- [ ] Codespace criado no meu fork
- [ ] VS Code conectado ao Codespace (ver "Codespaces: ..." no canto inferior esquerdo)

### Serviços Docker

No terminal do VS Code conectado ao Codespace, execute:

```bash
docker compose ps
```

- [ ] Container `minio` está "Up"
- [ ] Container `minio-create-bucket` está "Exited" (0) — isso é normal!
- [ ] Container `postgres` está "Up"
- [ ] Container `postgres-mlops` está "Up"
- [ ] Container `mlflow-server` está "Up"
- [ ] Container `client` está "Up"

**Se o mlflow-server não estiver Up:**
```bash
docker compose restart mlflow-server
docker compose logs mlflow-server
```

### Port Forwarding

No VS Code conectado ao Codespace:

- [ ] Painel PORTS está visível (View → Ports)
- [ ] Porta 5000 está "Forwarded"
- [ ] Porta 9001 está "Forwarded"
- [ ] Porta 5433 está "Forwarded" 
- [ ] Porta 5434 está "Forwarded"

### Acesso aos Serviços

No seu navegador local:

- [ ] http://localhost:5000 abre o MLflow UI
- [ ] http://localhost:9001 abre o MinIO Console
- [ ] Login do MinIO funciona (user: `user`, senha: `password`)

---

## 💻 Parte 2: Ambiente Local

### Git e Projeto

- [ ] Fork clonado localmente: `git clone https://github.com/SEU-USUARIO/mlops.git`
- [ ] Estou dentro do diretório do projeto: `cd mlops`
- [ ] Arquivos do projeto estão visíveis: `ls` mostra `.devcontainer`, `docker-compose.yml`, etc.

### Conda

Verifique a instalação:

```bash
conda --version
```

- [ ] Conda instalado (versão aparece)
- [ ] Ambiente criado: `conda env list` mostra `mlops-util-env`
- [ ] Ambiente ativado: `conda activate mlops-util-env`
- [ ] Prompt do terminal mostra `(mlops-util-env)`

### Pacotes Python

Com o ambiente ativado:

```bash
conda list
```

- [ ] `mlflow` está instalado
- [ ] `pandas` está instalado
- [ ] `scikit-learn` está instalado
- [ ] `jupyterlab` está instalado
- [ ] `ipykernel` está instalado

**Teste de import:**

```bash
python -c "import mlflow, pandas, sklearn, jupyterlab; print('✅ Todos os pacotes OK!')"
```

- [ ] Comando acima executou sem erros

### Jupyter Kernel

```bash
jupyter kernelspec list
```

- [ ] Kernel `mlops-util-env` está listado
- [ ] Caminho do kernel aponta para seu ambiente Conda

### VS Code Local

- [ ] VS Code aberto no diretório do projeto (`code .`)
- [ ] Extensão Python instalada no VS Code
- [ ] Extensão Jupyter instalada no VS Code
- [ ] Interpretador Python selecionado: **Python 3.13 (mlops-util-env)**

### Teste de Notebook

Abra: `notebooks/example_mlflow.ipynb`

- [ ] Notebook abre sem erros
- [ ] Seletor de kernel mostra **Python 3.13 (mlops-util-env)**
- [ ] Consigo selecionar o kernel
- [ ] Primeira célula executa sem erros
- [ ] Dados aparecem no MLflow (http://localhost:5000)

---

## 🔄 Parte 3: Integração (2 VS Codes)

### VS Code #1 - Codespace

- [ ] Está aberto e conectado ao Codespace
- [ ] Mostra "Codespaces: ..." no canto inferior esquerdo
- [ ] Terminal executa comandos Docker: `docker compose ps`
- [ ] Painel PORTS mostra as portas encaminhadas

### VS Code #2 - Local

- [ ] Está aberto no diretório do projeto local
- [ ] Mostra o caminho local no título da janela
- [ ] Terminal mostra prompt local (não do Codespace)
- [ ] Ambiente Conda ativado: `(mlops-util-env)` no terminal
- [ ] Notebooks abrem e executam corretamente

### Teste de Conectividade

No VS Code Local (terminal ou notebook):

```python
import mlflow
mlflow.set_tracking_uri('http://localhost:5000')
print(mlflow.get_tracking_uri())
print(mlflow.MlflowClient().list_experiments())
```

- [ ] Código executa sem erros
- [ ] URI está configurada como `http://localhost:5000`
- [ ] Consegue listar experimentos do MLflow

---

## 🎯 Parte 4: Fluxo de Trabalho

### Desenvolvimento

- [ ] Consigo editar notebooks no VS Code Local
- [ ] Consigo executar células dos notebooks
- [ ] Experimentos aparecem no MLflow (http://localhost:5000)
- [ ] Consigo ver artefatos no MinIO (http://localhost:9001)

### Git

No VS Code Local:

```bash
git status
git add .
git commit -m "Teste"
git push origin main
```

- [ ] `git status` funciona
- [ ] Consigo fazer commit
- [ ] Consigo fazer push para o meu fork

### Gerenciamento do Codespace

- [ ] Sei como parar os serviços: `docker compose down`
- [ ] Sei como parar o Codespace no GitHub
- [ ] Sei como reativar o Codespace quando necessário

---

## 🐛 Troubleshooting

Se algo não estiver funcionando:

### MLflow não abre

```bash
# No VS Code do Codespace
docker compose restart mlflow-server
docker compose logs mlflow-server
```

### Porta não encaminha

```
VS Code do Codespace → PORTS → Clique direito na porta → Forward Port
```

### Conda não encontra pacotes

```bash
conda install -c conda-forge -c anaconda --file requirements_conda.txt
```

### Kernel não aparece

```bash
conda activate mlops-util-env
python -m ipykernel install --user --name mlops-util-env --display-name "Python 3.13 (mlops-util-env)"
```

---

## ✅ Tudo OK?

Se todos os itens estão marcados, seu ambiente está pronto! 🎉

### Próximos passos:

1. Explore o notebook de exemplo
2. Crie seus próprios experimentos
3. Consulte a [Referência](./REFERENCE.md) para comandos úteis
4. Leia o [README](../README.md) para mais detalhes

---

**Lembre-se:** Sempre pare o Codespace quando terminar! ⚠️
