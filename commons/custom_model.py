import mlflow
from joblib import load
import configparser
import geopy.distance
from typing import Dict, Any, List, Union
import pandas as pd

import warnings
warnings.filterwarnings('ignore')

class CustomModel(mlflow.pyfunc.PythonModel):

    def __init__(self, env = 'PROD'):
        
        self.env = env
        self.app_config = self.get_app_config('config/app_config.ini')

    def load_context(self, context):

        app_config_path = context.artifacts["app_config"]
        model_path = context.artifacts["model"]

        # Load app config
        self.app_config = self.get_app_config(app_config_path)
        
        # Load model
        self.model = load(model_path)

        # Load config variables
        self.covered_region_in_km = int(self.app_config[self.env]['covered_region_in_km'])
        self.model_name = self.app_config['ALL']['model_name']
        
    # Carrega das configurações da aplicação
    def get_app_config (self, app_config_path):

        app_config = configparser.ConfigParser()
        app_config.read(app_config_path)
        return app_config
        
    def predict(self, context, model_input: Dict[str, Any]) -> Dict[str, Any]:
       
        if 'method' not in model_input:
            raise ValueError("Input must contain a 'method' key to specify the operation")

        method = model_input['method']
        data = model_input['data']

        if method == 'predict':
            return self.make_predictions(data, self.model, self.covered_region_in_km)
        
        elif method == 'get_cluster_centroids':
            return self.get_cluster_centroids()

        elif method == 'get_model_version':
            model_uri, run_id, version  = self.get_model_uri_by_name_and_alias('prod.{}'.format(self.model_name), 'champion')
            return {
                'version': version,
                'run_id': run_id,
                'model_uri': model_uri
            }
            
        else:
            raise ValueError(f"Unknown method: {method}")
    
    def get_model_uri_by_name_and_alias(self, model_name, alias):

        # Initialize MLflow client
        client = mlflow.tracking.MlflowClient()
        
        # Get the model version details by alias
        model_version_details = client.get_model_version_by_alias(name=model_name, alias=alias)
        
        # Construct the model URI
        model_uri = f"models:/{model_name}/{model_version_details.version}"
        
        return model_uri, model_version_details.run_id, model_version_details.version
        
    def make_predictions(self, data: List[float], model, covered_region_in_km: int) -> Dict[str, Any]:
        
        # Prepara as coordenadas do CEP
        coords_cep = (data[0], data[1])
    
        # Lista centróides dos clusters
        centers = self.get_cluster_centroids()
    
        # Verifica a distância (em km) entre o CEP a cada cluster
        res = dict()
        for c in centers:
            coords_cluster = (c['lat'], c['lng'])
            res[c['cluster']] = geopy.distance.geodesic(coords_cep, coords_cluster).km
    
        # Cria uma lista com as chaves (keys) ordenadas pelos seus valores (values)
        res_sorted_keys = sorted(res, key=res.get, reverse=False)
        
        # Prepara o resultado do endpoint
        results = {
            'is_region_covered': round(res[res_sorted_keys[0]], 2) <= covered_region_in_km,
            'closest_center': {
                'id': res_sorted_keys[0],
                'distance_in_km': round(res[res_sorted_keys[0]], 2),
                # res_sorted_keys é uma lista, sendo que a primeira posição (cluster 1) eh igual a 0
                'lat': centers[res_sorted_keys[0] - 1]['lat'],
                'lng': centers[res_sorted_keys[0] - 1]['lng']
            }
        }

        return results
    
    # Retorna os centróides de cada cluster
    def get_cluster_centroids(self) -> List[Dict[str, Any]]:
        
        centers = []
        for i, center in enumerate(self.model.cluster_centers_):
            c = dict()
            c['lat'] = center[0]
            c['lng'] = center[1]
            c['cluster'] = i + 1
            centers.append(c)
            
        return centers