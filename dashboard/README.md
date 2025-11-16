# 📊 Drift Monitor Dashboard

Dashboard interativo para monitoramento de drift do modelo de clustering usando MLflow Traces.

## 🚀 Instalação

```bash
pip install -r requirements/requirements_dashboard.txt
```

## ▶️ Como Executar

```bash
streamlit run dashboard/drift_monitor.py
```

O dashboard estará disponível em: `http://localhost:8501`

## 📋 Funcionalidades

### 1️⃣ **Métricas Principais**
- Total de traces analisados
- Taxa de cobertura da região
- Distância média das predições
- Latência média da API

### 2️⃣ **Timeline de Requisições**
- Visualização do volume de requisições por hora
- Identificação de picos de tráfego

### 3️⃣ **Análise de Drift por Cluster**
- Detecção automática de concept drift (desvio ≥ 5%)
- Comparação: cobertura atual vs referência
- Distribuição de distâncias
- Latência ao longo do tempo
- Status visual (🟢 OK / 🔴 DRIFT)

### 4️⃣ **Relatório Evidently AI**
- Testes estatísticos automáticos (PSI, KS, Chi²)
- Análise de drift em múltiplas features
- Relatório HTML interativo

## ⚙️ Configurações

No sidebar você pode ajustar:
- **Experimento MLflow**: Nome do experimento (default: `mlops-experiment`)
- **Janela temporal**: Quantas horas de histórico analisar (1-168h)
- **Máximo de traces**: Limite de traces a buscar (50-1000)

## 🔄 Atualização Automática

O dashboard tem cache de 5 minutos. Para forçar atualização:
1. Clique no botão "🔄 Atualizar" no sidebar
2. Ou aguarde o cache expirar automaticamente

## 📊 Fonte de Dados

**MLflow Traces** - Extrai dados diretamente dos traces do experimento:
- Inputs: latitude, longitude
- Outputs: predições (região coberta, cluster, distância)
- Metadados: timestamp, latência, status

## ⚠️ Pré-requisitos

1. **MLflow Server** rodando em `http://localhost:5000`
2. **API** gerando traces (predições na rota `/get-delivery-region`)
3. **Arquivo drift_params.joblib** gerado pelo treinamento (em `temp/`)

## 🎯 Lógica de Drift

Drift é detectado quando:
```
desvio = 1 - (cobertura_atual / cobertura_referência)
```

Se `desvio >= 5%` → **DRIFT DETECTADO** 🔴

Isso indica que os clientes estão requisitando mais predições fora da região de entrega.

## 📈 Exemplo de Uso

```bash
# 1. Inicie o MLflow
mlflow server --host 0.0.0.0 --port 5000

# 2. Inicie a API
uvicorn api.main:app --reload

# 3. Gere algumas predições
curl http://localhost:8000/get-delivery-region/-23.5505/-46.6333

# 4. Inicie o dashboard
streamlit run dashboard/drift_monitor.py
```

## 🐛 Troubleshooting

**Erro: "Nenhum trace encontrado"**
- Execute predições na API primeiro
- Verifique se o experimento está correto
- Confirme que o MLflow está rodando

**Erro: "drift_params.joblib não encontrado"**
- Execute o notebook de treinamento (`bootcamp-project-part-X.ipynb`)
- Certifique-se que o arquivo está em `temp/drift_params.joblib`

**Relatório Evidently não gera**
- São necessários pelo menos 40 traces
- Verifique instalação: `pip install evidently`

## 🔗 Links Úteis

- MLflow UI: http://localhost:5000
- MLflow Traces: http://localhost:5000/#/traces
- API Docs: http://localhost:8000/docs
