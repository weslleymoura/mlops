# 🚀 Guia Rápido — Setup em 5 Passos# 🚀 Guia Rápido: Setup em 5 minutos



Configure seu ambiente híbrido de MLOps em 15 minutos.## ✅ Pré-requisitos (Instalar uma vez)



---1. **VS Code** instalado → [Download](https://code.visualstudio.com/)

2. **Extensão GitHub Codespaces** no VS Code:

## Passo 1: Fork do Projeto (2 min)   - Abra o VS Code

   - Pressione `Ctrl+Shift+X`

1. Acesse: https://github.com/weslleymoura/mlops   - Procure: "GitHub Codespaces"

2. Clique em **Fork** (canto superior direito)   - Clique em "Install"

3. Aguarde criação do fork na sua conta

---

✅ Agora você tem sua própria cópia do projeto!

## 🎯 Setup em 3 Passos

---

### 1️⃣ Criar o Codespace (2 minutos)

## Passo 2: Criar Codespace (3 min)

No GitHub, neste repositório:

No **seu fork**:

```

1. Clique em **Code** → **Codespaces** → **Create codespace on main**Code → Codespaces → Create codespace on main

2. Aguarde 2-3 minutos```

3. Os serviços serão instalados automaticamente

Aguarde 2-3 minutos. O Codespace vai configurar tudo automaticamente.

✅ MLflow, MinIO e Postgres estarão rodando no Codespace!

---

---

### 2️⃣ Conectar VS Code Local (1 minuto)

## Passo 3: Conectar VS Code ao Codespace (1 min)

**Opção A: Pelo VS Code**

No seu **VS Code local**:```

Ctrl+Shift+P → "Codespaces: Connect to Codespace" → Selecione o codespace

1. Pressione `Ctrl+Shift+P` (ou `Cmd+Shift+P`)```

2. Digite: `Codespaces: Connect to Codespace`

3. Selecione seu Codespace**Opção B: Pelo GitHub** 

```

✅ Este será seu **VS Code #1** (apenas para serviços)GitHub → Codespaces → [...] → Open in Visual Studio Code

```

**Teste:** Abra http://localhost:5000 no navegador (deve mostrar MLflow)---



---### 3️⃣ Testar (30 segundos)



## Passo 4: Clonar Fork Localmente (2 min)1. **Verifique a conexão:**

   - Canto inferior esquerdo do VS Code: **> Codespaces: [nome]** ✅

```bash

# Substituir SEU-USUARIO2. **Abra o MLflow:**

git clone https://github.com/SEU-USUARIO/mlops.git   - Navegador: http://localhost:5000 ✅

cd mlops

```3. **Verifique os containers:**

   - Terminal do VS Code: `docker compose ps` ✅

✅ Projeto clonado no seu computador!

---

---

## 🎉 Pronto! Agora você pode:

## Passo 5: Configurar Ambiente Conda (7 min)

### 📓 Executar o notebook

```bash```

# Criar ambienteNo VS Code: notebooks/example_mlflow.ipynb → Run All

conda create -n mlops-util-env python=3.13```



# Ativar### 🌐 Acessar os serviços

conda activate mlops-util-env

| Serviço | URL | Login |

# Instalar dependências|---------|-----|-------|

conda install -c conda-forge --file requirements_conda.txt| MLflow UI | http://localhost:5000 | - |

| MinIO Console | http://localhost:9001 | user / password |

# Registrar kernel

python -m ipykernel install --user --name mlops-util-env --display-name "Python 3.13 (mlops-util-env)"### 🐳 Comandos Docker úteis



# Abrir VS Code local```bash

code .# Ver status

```docker compose ps



✅ Este será seu **VS Code #2** (desenvolvimento)# Ver logs do MLflow

docker logs -f mlops-mlflow-server-1

---

# Reiniciar MLflow

## ✅ Pronto! Agora você tem:docker restart mlops-mlflow-server-1

```

- ✅ **VS Code #1**: Conectado ao Codespace (serviços rodando)

- ✅ **VS Code #2**: Local com projeto e ambiente Conda---

- ✅ **Navegador**: Acesso aos serviços via localhost

## 🛑 Ao Terminar

---

```bash

## 🎯 Teste Rápido# 1. Parar serviços no terminal do VS Code

docker compose down

No **VS Code #2** (local), abra o notebook `notebooks/example_mlflow.ipynb`:

# 2. Fechar VS Code (ou desconectar: Ctrl+Shift+P → Close Remote Connection)

1. Selecione o kernel: **Python 3.13 (mlops-util-env)**

2. Execute a primeira célula# 3. Parar o Codespace no GitHub

3. Vá em http://localhost:5000https://github.com/codespaces → [...] → Stop codespace

4. Veja o experimento registrado no MLflow!```



---**� Importante:** Sempre pare o Codespace para economizar créditos!



## 💡 Próximos Passos---



- 📋 [Checklist Completo](./CHECKLIST.md) - Verificar tudo## 🐛 Problemas?

- 📚 [Referência](./REFERENCE.md) - Comandos úteis

- 📖 [README Principal](../README.md) - Documentação completa### MLflow não abre

```bash

---docker restart mlops-mlflow-server-1

# Aguarde 10 segundos e acesse novamente

## ⚠️ Lembre-se```



Ao terminar:### Porta não funciona

1. No VS Code do Codespace: `docker compose down````

2. No GitHub: Parar o Codespace (https://github.com/codespaces)VS Code → Painel PORTS (View → Ports) → Clique direito → Forward Port → Digite 5000

```

### Codespace não conecta
```
Feche o VS Code → Abra novamente → Tente conectar de novo
```

---

📚 **Documentação completa**: [README.md](../README.md)
✅ **Checklist detalhado**: [CHECKLIST.md](./CHECKLIST.md)
📌 **Referência de comandos**: [REFERENCE.md](./REFERENCE.md)
