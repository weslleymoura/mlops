"""
Drift Monitor Dashboard - MLflow Traces
Monitora drift de predições usando traces do MLflow
"""
import streamlit as st
import pandas as pd
import mlflow
from mlflow.tracking import MlflowClient
from evidently import Report
from evidently.presets import DataDriftPreset
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Drift Monitor", layout="wide")
st.title("🔍 Monitoramento de Drift - Delivery Region (MLflow Traces)")

# Conecta ao MLflow
@st.cache_resource
def get_mlflow_client():
    tracking_uri = os.getenv('MLFLOW_TRACKING_URI', 'http://localhost:5000')
    mlflow.set_tracking_uri(tracking_uri)
    return MlflowClient()

# Carrega traces do MLflow
@st.cache_data(ttl=300)  # Cache de 5 minutos
def load_traces_data(experiment_name, max_results=500, hours_back=24):
    """
    Carrega traces do MLflow e extrai dados de predições.
    
    Args:
        experiment_name: Nome do experimento
        max_results: Máximo de traces a buscar
        hours_back: Quantas horas atrás buscar
    """
    client = get_mlflow_client()
    
    # Busca experimento
    experiment = client.get_experiment_by_name(experiment_name)
    if not experiment:
        st.error(f"Experimento '{experiment_name}' não encontrado!")
        return pd.DataFrame()
    
    # Busca traces
    traces = client.search_traces(
        locations=[experiment.experiment_id],
        max_results=max_results,
        order_by=["timestamp_ms DESC"]
    )
    
    # Extrai dados dos traces
    data = []
    for trace in traces:
        # Filtra apenas traces de predição
        if trace.info.tags.get('mlflow.traceName') == 'predict_delivery_region':
            
            # Extrai inputs e outputs dos spans
            trace_data = {
                'trace_id': trace.info.request_id,
                'timestamp': datetime.fromtimestamp(trace.info.timestamp_ms / 1000),
                'status': trace.info.status,
                'execution_time_ms': trace.info.execution_time_ms
            }
            
            # Percorre spans para extrair dados
            for span in trace.data.spans:
                if span.name == 'predict':
                    # Inputs (lat, lng)
                    if span.inputs:
                        trace_data['lat'] = span.inputs.get('lat')
                        trace_data['lng'] = span.inputs.get('lng')
                    
                    # Outputs (resultado da predição)
                    if span.outputs:
                        result = span.outputs
                        trace_data['res_is_region_covered'] = result.get('is_region_covered')
                        trace_data['res_closest_center_id'] = result.get('closest_center', {}).get('id')
                        trace_data['res_closest_center_distance_in_km'] = result.get('closest_center', {}).get('distance_in_km')
                        trace_data['res_closest_center_lat'] = result.get('closest_center', {}).get('lat')
                        trace_data['res_closest_center_lng'] = result.get('closest_center', {}).get('lng')
            
            # Adiciona apenas se tem dados completos
            if 'lat' in trace_data and 'res_is_region_covered' in trace_data:
                data.append(trace_data)
    
    df = pd.DataFrame(data)
    
    # Filtra por tempo
    if not df.empty and hours_back:
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        df = df[df['timestamp'] >= cutoff_time]
    
    return df

# Carrega dados de referência (treino)
@st.cache_data
def load_reference_data():
    from joblib import load
    drift_params = load('temp/drift_params.joblib')
    return drift_params

# Sidebar - Configurações
st.sidebar.header("⚙️ Configurações")

experiment_name = st.sidebar.text_input(
    "Experimento MLflow", 
    value="mlops-experiment"
)

hours_back = st.sidebar.slider(
    "Janela temporal (horas)", 
    1, 168, 24
)

max_traces = st.sidebar.slider(
    "Máximo de traces", 
    50, 1000, 500
)

refresh = st.sidebar.button("🔄 Atualizar")

# Info sobre MLflow
mlflow_uri = os.getenv('MLFLOW_TRACKING_URI', 'http://localhost:5000')
st.sidebar.info(f"📊 MLflow: {mlflow_uri}")
st.sidebar.info(f"🔬 Experimento: {experiment_name}")

# Carrega dados
with st.spinner("Carregando traces do MLflow..."):
    df_current = load_traces_data(experiment_name, max_traces, hours_back)
    
    try:
        drift_params = load_reference_data()
    except Exception as e:
        st.error(f"Erro ao carregar drift_params.joblib: {e}")
        st.info("Execute o notebook de treinamento para gerar os parâmetros de drift.")
        st.stop()

if df_current.empty:
    st.warning("⚠️ Nenhum trace encontrado. Execute algumas predições na API primeiro.")
    st.info("Exemplo: curl http://localhost:8000/get-delivery-region/-23.5505/-46.6333")
    st.stop()

# Métricas principais
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Traces", len(df_current))
with col2:
    coverage_rate = (df_current['res_is_region_covered'].sum() / len(df_current)) * 100
    st.metric("Taxa de Cobertura", f"{coverage_rate:.1f}%")
with col3:
    avg_distance = df_current['res_closest_center_distance_in_km'].mean()
    st.metric("Distância Média", f"{avg_distance:.2f} km")
with col4:
    avg_latency = df_current['execution_time_ms'].mean()
    st.metric("Latência Média", f"{avg_latency:.0f} ms")

# Timeline de requests
st.divider()
st.header("📈 Timeline de Requisições")

df_timeline = df_current.set_index('timestamp').resample('1h').size().reset_index(name='count')
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df_timeline['timestamp'],
    y=df_timeline['count'],
    mode='lines+markers',
    name='Requisições/hora',
    line=dict(color='steelblue', width=2),
    marker=dict(size=8)
))
fig.update_layout(
    title="Volume de Requisições por Hora",
    xaxis_title="Timestamp",
    yaxis_title="Número de Requisições",
    height=300,
    hovermode='x unified'
)
st.plotly_chart(fig, width="stretch")

# Separador
st.divider()

# Análise por Cluster
st.header("📊 Análise de Drift por Cluster")

# Resumo de todos os clusters
clusters_summary = []
for cluster_id in sorted(df_current['res_closest_center_id'].unique()):
    cluster_data = df_current[df_current['res_closest_center_id'] == cluster_id]
    
    if len(cluster_data) >= 20 and cluster_id in drift_params:
        current_coverage = (cluster_data['res_is_region_covered'].sum() / len(cluster_data))
        reference_coverage = drift_params[cluster_id]['perc_inner_radius']
        deviation = 1 - (current_coverage / reference_coverage)
        drift_detected = deviation >= 0.05
        
        clusters_summary.append({
            'Cluster': cluster_id,
            'Traces': len(cluster_data),
            'Cobertura Atual': f"{current_coverage:.1%}",
            'Cobertura Ref.': f"{reference_coverage:.1%}",
            'Desvio': f"{deviation:.1%}",
            'Status': '🔴 DRIFT' if drift_detected else '🟢 OK'
        })

if clusters_summary:
    st.dataframe(pd.DataFrame(clusters_summary), width="stretch", hide_index=True)
else:
    st.warning("Nenhum cluster com dados suficientes para análise (mínimo: 20 traces)")

st.divider()

# Análise detalhada por cluster
for cluster_id in sorted(df_current['res_closest_center_id'].unique()):
    cluster_data = df_current[df_current['res_closest_center_id'] == cluster_id]
    
    if len(cluster_data) >= 20 and cluster_id in drift_params:
        with st.expander(f"🎯 Cluster {cluster_id} ({len(cluster_data)} traces)"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                # Taxa de cobertura atual vs referência
                current_coverage = (cluster_data['res_is_region_covered'].sum() / len(cluster_data))
                reference_coverage = drift_params[cluster_id]['perc_inner_radius']
                deviation = 1 - (current_coverage / reference_coverage)
                
                # Alerta de drift
                drift_detected = deviation >= 0.05
                if drift_detected:
                    st.error(f"⚠️ **DRIFT DETECTADO!**")
                    st.metric("Desvio", f"{deviation:.1%}", delta=f"{deviation:.1%}", delta_color="inverse")
                else:
                    st.success(f"✅ **Sem drift**")
                    st.metric("Desvio", f"{deviation:.1%}")
                
                # Comparação
                st.metric("Cobertura Atual", f"{current_coverage:.1%}")
                st.metric("Cobertura Referência", f"{reference_coverage:.1%}")
            
            with col2:
                # Gráfico de comparação
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=['Referência', 'Atual'],
                    y=[reference_coverage * 100, current_coverage * 100],
                    marker_color=['lightblue', 'red' if drift_detected else 'green'],
                    text=[f"{reference_coverage:.1%}", f"{current_coverage:.1%}"],
                    textposition='auto'
                ))
                fig.update_layout(
                    title="Taxa de Cobertura (%)",
                    yaxis_range=[0, 100],
                    height=300,
                    showlegend=False
                )
                st.plotly_chart(fig, width="stretch")
            
            with col3:
                # Distribuição de distâncias
                fig = go.Figure()
                fig.add_trace(go.Histogram(
                    x=cluster_data['res_closest_center_distance_in_km'],
                    nbinsx=20,
                    marker_color='steelblue'
                ))
                fig.update_layout(
                    title="Distribuição de Distâncias (km)",
                    xaxis_title="Distância (km)",
                    yaxis_title="Frequência",
                    height=300,
                    showlegend=False
                )
                st.plotly_chart(fig, width="stretch")
            
            # Latência ao longo do tempo
            st.subheader("⏱️ Latência ao Longo do Tempo")
            cluster_timeline = cluster_data.sort_values('timestamp')
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=cluster_timeline['timestamp'],
                y=cluster_timeline['execution_time_ms'],
                mode='markers',
                marker=dict(
                    color=cluster_timeline['res_is_region_covered'].map({True: 'green', False: 'red'}),
                    size=8
                ),
                text=cluster_timeline['res_is_region_covered'].map({True: 'Coberto', False: 'Não Coberto'}),
                hovertemplate='<b>%{text}</b><br>Latência: %{y:.0f}ms<br>%{x}<extra></extra>'
            ))
            fig.update_layout(
                xaxis_title="Timestamp",
                yaxis_title="Latência (ms)",
                height=250
            )
            st.plotly_chart(fig, width="stretch")

# Separador
st.divider()

# Evidently Report
st.header("📈 Relatório Evidently AI")

col1, col2 = st.columns([3, 1])
with col1:
    st.info("💡 Gere um relatório detalhado com testes estatísticos de drift (PSI, KS, Chi²)")
with col2:
    generate_report = st.button("🔬 Gerar Relatório", type="primary", width="stretch")

if generate_report:
    if len(df_current) < 40:
        st.warning("⚠️ São necessários pelo menos 40 traces para gerar o relatório Evidently.")
    else:
        with st.spinner("Gerando relatório Evidently..."):
            try:
                # Separa dados em referência e atual
                split_idx = len(df_current) // 2
                df_reference = df_current.iloc[:split_idx].copy()
                df_production = df_current.iloc[split_idx:].copy()
                
                # Cria relatório com DataDriftPreset
                report = Report(metrics=[
                    DataDriftPreset(),
                ])
                
                report.run(
                    reference_data=df_reference,
                    current_data=df_production
                )
                
                # Exibe relatório
                st.components.v1.html(report.get_html(), height=1200, scrolling=True)
            
            except Exception as e:
                st.error(f"Erro ao gerar relatório Evidently: {e}")
                st.info("Certifique-se de que o pacote evidently está instalado: pip install evidently")

# Summary
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Dados do Dashboard")
    st.write(f"- **Período**: Últimas {hours_back}h")
    st.write(f"- **Total de traces**: {len(df_current)}")
    st.write(f"- **Clusters ativos**: {df_current['res_closest_center_id'].nunique()}")
    if not df_current.empty:
        st.write(f"- **Timestamps**: {df_current['timestamp'].min().strftime('%Y-%m-%d %H:%M')} → {df_current['timestamp'].max().strftime('%Y-%m-%d %H:%M')}")

with col2:
    st.subheader("🔄 Atualização")
    st.write("- Cache: 5 minutos")
    st.write("- Fonte: MLflow Traces")
    st.write(f"- Última atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Footer
st.divider()
st.caption(f"🔗 [MLflow UI]({mlflow_uri}/#/traces) | 🔄 Dashboard atualizado automaticamente a cada 5 minutos")
