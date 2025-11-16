import os
import sys 
from pathlib import Path
path = Path().joinpath().joinpath('..')
sys.path.append(str(path))

from dotenv import load_dotenv
load_dotenv()

import configparser

from fastapi import FastAPI
from src.delivery_region_mlflow import DeliveryRegion
import mlflow

# Load app config from /api
app_config = configparser.ConfigParser()
app_config.read('config/app_config.ini')

# Determine environment
env = os.getenv('ENV')
tracing_group = app_config[env]['tracing_group']

# MLFlow server
tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
mlflow.set_tracking_uri(tracking_uri)
mlflow.set_experiment(tracing_group)

# Instancia um objeto da classe DeliveryRegion, que contém algumas lógicas da API
delivery_region = DeliveryRegion()

# Carrega a versão de produção do modelo de clustering
clustering_model_name = 'prod.mlops.kmeans-clustering'
clustering_alias = 'champion'
clustering_model_uri, clustering_run_id = delivery_region.get_model_uri_by_name_and_alias(
    clustering_model_name, 
    clustering_alias
)
loaded_clustering_model = mlflow.pyfunc.load_model(clustering_model_uri)

app = FastAPI()

@app.get("/", summary="MLOps root path")
async def mlops():
    return {"message": "Bem-vindo ao curso de MLOps!"}

@app.get("/get-delivery-region/{lat}/{lng}", summary="Valida região de entrega")
@mlflow.trace(name="predict_delivery_region", span_type="CHAIN")
def get_delivery_region(lat, lng):
    
    with mlflow.start_span(name="load_model") as span:
        span.set_inputs({"model": clustering_model_name, "alias": clustering_alias})
        model_uri, run_id = delivery_region.get_model_uri_by_name_and_alias(
            clustering_model_name, 
            clustering_alias
        )
        loaded_model = mlflow.pyfunc.load_model(model_uri)
        span.set_outputs({"model_uri": model_uri, "run_id": run_id})

    with mlflow.start_span(name="predict") as span:
        span.set_inputs({"lat": float(lat), "lng": float(lng)})
        data = {
            'method': 'predict',
            'data': [lat, lng]
        } 
        result = loaded_model.predict(data)
        span.set_outputs(result)

    return result

@app.get("/get-model-version", summary="Retorna a versão da API")
@mlflow.trace(name="get_model_version", span_type="RETRIEVER")
def get_model_version():
    
    with mlflow.start_span(name="load_model") as span:
        span.set_inputs({"model": clustering_model_name, "alias": clustering_alias})
        model_uri, run_id = delivery_region.get_model_uri_by_name_and_alias(
            clustering_model_name, 
            clustering_alias
        )
        loaded_model = mlflow.pyfunc.load_model(model_uri)
        span.set_outputs({"model_uri": model_uri, "run_id": run_id})

    with mlflow.start_span(name="get_version") as span:
        data = {
            'method': 'get_model_version',
            'data': None
        }
        result = loaded_model.predict(data)
        span.set_outputs(result)
    
    return result

@app.get("/get-clusters", summary="Retorna os centróides de cada cluster")
@mlflow.trace(name="get_clusters", span_type="RETRIEVER")
def get_cluster():
    
    with mlflow.start_span(name="load_model") as span:
        span.set_inputs({"model": clustering_model_name, "alias": clustering_alias})
        model_uri, run_id = delivery_region.get_model_uri_by_name_and_alias(
            clustering_model_name, 
            clustering_alias
        )
        loaded_model = mlflow.pyfunc.load_model(model_uri)
        span.set_outputs({"model_uri": model_uri, "run_id": run_id})

    with mlflow.start_span(name="get_centroids") as span:
        data = {
            'method': 'get_cluster_centroids',
            'data': None
        }
        result = loaded_model.predict(data)
        span.set_outputs(result)
    
    return result

