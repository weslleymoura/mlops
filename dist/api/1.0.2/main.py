import os

# Variáveis de ambiente
os.environ['AWS_ACCESS_KEY_ID'] = 'user'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'password'
os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'http://localhost:9000'
os.environ['DATABASE_URL'] = 'postgresql://bootcamp_user:admin@localhost:5434/bootcamp_db'

from fastapi import FastAPI, HTTPException
from src.delivery_region_mlflow import DeliveryRegion
import brazilcep
from geopy.geocoders import Nominatim
import geopy.distance
from joblib import load
from pathlib import Path
import sys 
import mlflow
path = Path().joinpath().joinpath('..')
sys.path.append(str(path))
from src.database import SessionLocal, engine
from src import models, schemas
from sqlalchemy.orm import Session
from fastapi import Query, Depends

# Prepara o banco de dados
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 

# MLFlow server
mlflow.set_tracking_uri("http://localhost:5000")

# Instancia um objeto da classe DeliveryRegion, que contém algumas lógicas da API
delivery_region = DeliveryRegion()

# Carrega a versão de produção do modelo
model_name = 'prod.bootcamp.kmeans-clustering'
alias = 'champion'
model_uri, run_id = delivery_region.get_model_uri_by_name_and_alias(model_name, alias)
loaded_model = mlflow.pyfunc.load_model(model_uri)

app = FastAPI()

@app.get("/", summary="Bootcamp root parh")
async def bootcamp():
    return {"message": "Bem-vindo ao bootcamp!"}

@app.get("/get-delivery-region/{lat}/{lng}", summary="Valida região de entrega")
def get_delivery_region(lat, lng, db: Session = Depends(get_db)):

    model_uri, run_id = delivery_region.get_model_uri_by_name_and_alias(model_name, alias)
    loaded_model = mlflow.pyfunc.load_model(model_uri)

    data = {
        'method': 'predict',
        'data': [lat, lng]
    } 
    result = loaded_model.predict(data)

    # Registra a chamada da API no banco de dados
    new_api_call = models.ApiCall(
        lat=lat, 
        lng=lng,
        res_is_region_covered = result['is_region_covered'],
        res_closest_center_id = result['closest_center']['id'],
        res_closest_center_distance_in_km = result['closest_center']['distance_in_km'],
        res_closest_center_lat = result['closest_center']['lat'],
        res_closest_center_lng = result['closest_center']['lng'])

    # Add the user to the session
    db.add(new_api_call)

    # Commit the session to persist the changes
    db.commit()

    # Close the session
    db.close()

    return result

@app.get("/get-model-version", summary="Retorna a versão da API")
def get_model_version():

    model_uri, run_id = delivery_region.get_model_uri_by_name_and_alias(model_name, alias)
    loaded_model = mlflow.pyfunc.load_model(model_uri)

    data = {
        'method': 'get_model_version',
        'data': None
    } 
    return loaded_model.predict(data)

@app.get("/get-clusters", summary="Retorna os centróides de cada cluster")
def get_cluster():

    model_uri, run_id = delivery_region.get_model_uri_by_name_and_alias(model_name, alias)
    loaded_model = mlflow.pyfunc.load_model(model_uri)

    data = {
        'method': 'get_cluster_centroids',
        'data': None
    } 
    return loaded_model.predict(data)