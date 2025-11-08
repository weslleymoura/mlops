# ✅ Checklist de Configuração: VS Code Local + Codespace

## 📋 Antes de Começar

- [ ] Tenho uma conta no GitHub
- [ ] VS Code está instalado no meu computador
- [ ] Extensão "GitHub Codespaces" está instalada no VS Code
- [ ] Fiz fork deste repositório (ou tenho acesso)

## 🚀 Passo 1: Criar o Codespace

- [ ] Abri o repositório no GitHub
- [ ] Cliquei em **Code** → **Codespaces**
- [ ] Cliquei em **Create codespace on main**
- [ ] Aguardei a criação (pode levar 2-3 minutos)
- [ ] Vi a mensagem "Codespace criado com sucesso"

## 🔌 Passo 2: Conectar VS Code Local

### Método 1: Pelo VS Code
- [ ] Abri o VS Code no meu computador
- [ ] Pressionei `Ctrl+Shift+P` (ou `Cmd+Shift+P` no Mac)
- [ ] Digitei: "Codespaces: Connect to Codespace"
- [ ] Selecionei o Codespace da lista
- [ ] Aguardei a conexão

### Método 2: Pelo GitHub (Alternativa)
- [ ] No GitHub, cliquei nos **[...]** ao lado do Codespace
- [ ] Selecionei "Open in Visual Studio Code"
- [ ] O VS Code abriu automaticamente

## ✔️ Passo 3: Verificar Conexão

- [ ] No canto inferior esquerdo do VS Code vejo: **> Codespaces: [nome]**
- [ ] Abri o terminal integrado (`Ctrl+``)
- [ ] O terminal mostra o prompt do Codespace
- [ ] Executei `docker compose ps` e vi os containers

## 🌐 Passo 4: Verificar Portas

- [ ] Abri o painel **PORTS** (View → Ports ou `Ctrl+Shift+P` → "Ports: Focus on Ports View")
- [ ] Vejo as seguintes portas listadas:

| Porta | Status | Serviço |
|-------|--------|---------|
| 5000 | ✅ Forwarded | MLflow UI |
| 9001 | ✅ Forwarded | MinIO Console |
| 9000 | ✅ Forwarded | MinIO API |
| 5433 | ✅ Forwarded | Postgres (MLflow) |
| 5434 | ✅ Forwarded | Postgres (MLOps) |

- [ ] Se alguma porta não estiver encaminhada:
  - [ ] Cliquei com botão direito na porta
  - [ ] Selecionei "Forward Port"
  - [ ] Digitei o número da porta

## 🧪 Passo 5: Testar os Serviços

### MLflow UI
- [ ] Abri o navegador em: http://localhost:5000
- [ ] Vejo a interface do MLflow
- [ ] Vejo "Default" no experimento

### MinIO Console
- [ ] Abri o navegador em: http://localhost:9001
- [ ] Fiz login com:
  - [ ] Usuário: `user`
  - [ ] Senha: `password`
- [ ] Vejo o bucket "bucket" criado

### Containers Docker
- [ ] No terminal do VS Code, executei: `docker compose ps`
- [ ] Todos os containers estão "Up":
  - [ ] `mlops-minio-1`
  - [ ] `mlops-postgres-1`
  - [ ] `mlops-postgres-mlops-1`
  - [ ] `mlops-mlflow-server-1`
  - [ ] `mlops-client-1`

## 📓 Passo 6: Testar Notebook

- [ ] No VS Code, naveguei até `notebooks/example_mlflow.ipynb`
- [ ] Abri o notebook
- [ ] Selecionei o kernel Python (mlops-util-env)
- [ ] Executei a primeira célula
- [ ] Executei todas as células (`Run All`)
- [ ] Vi o experimento aparecer no MLflow UI

## ✅ Verificação Final

### No VS Code Local:
- [ ] Consigo editar arquivos
- [ ] Consigo executar comandos no terminal
- [ ] Consigo fazer commits Git
- [ ] As extensões funcionam

### No Navegador:
- [ ] http://localhost:5000 → MLflow funciona
- [ ] http://localhost:9001 → MinIO funciona
- [ ] Vejo experimentos no MLflow

### No Codespace:
- [ ] Containers estão rodando (`docker compose ps`)
- [ ] Não há erros nos logs (`docker compose logs`)

## 🎯 Tudo Funcionando!

Se você marcou todos os itens acima, está tudo pronto! 🎉

### Próximos Passos:
1. Explore o notebook `example_mlflow.ipynb`
2. Crie seus próprios experimentos
3. Consulte o [README.md](./README.md) para mais detalhes

---

## ❌ Problemas?

### Porta não funciona
- [ ] Abri o painel PORTS
- [ ] Verifiquei se está "Forwarded"
- [ ] Cliquei direito → "Forward Port" se necessário
- [ ] Testei novamente no navegador

### MLflow não abre
```bash
# Executei no terminal:
docker restart mlops-mlflow-server-1
docker logs -f mlops-mlflow-server-1
```
- [ ] Aguardei 10 segundos
- [ ] Testei http://localhost:5000 novamente

### Codespace não conecta
- [ ] Verifiquei minha conexão com internet
- [ ] Fechei e reabri o VS Code
- [ ] Tentei novamente: `Ctrl+Shift+P` → "Codespaces: Connect to Codespace"

### Containers não estão rodando
```bash
# Executei no terminal:
docker compose down
docker compose up -d
docker compose ps
```
- [ ] Aguardei 30 segundos
- [ ] Verifiquei o status novamente

---

## 💡 Dicas

✅ **Para economizar créditos do GitHub:**
- Sempre execute `docker compose down` ao terminar
- Pare o Codespace no GitHub quando não estiver usando

✅ **Para melhor performance:**
- Mantenha apenas um Codespace ativo por vez
- Execute `docker system prune` periodicamente

✅ **Para desenvolvimento eficiente:**
- Use o terminal do VS Code (roda no Codespace)
- Salve arquivos normalmente (são salvos no Codespace)
- Faça commits/push normalmente (Git funciona igual)

---

📚 **Documentação Completa**: [README.md](./README.md)
🚀 **Guia Rápido**: [QUICKSTART.md](./QUICKSTART.md)
