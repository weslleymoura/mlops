from mlflow import MlflowClient
import mlflow
import argparse
from pathlib import Path
import os
import sys
from dotenv import load_dotenv
import configparser

load_dotenv()

def main(model_name, version):
 
    # Busca o tracking URI das variáveis de ambiente
    tracking_uri = os.getenv('MLFLOW_TRACKING_URI')
    
    # Configura o tracking URI
    mlflow.set_tracking_uri(tracking_uri)
    client = MlflowClient(tracking_uri=tracking_uri)
    
    print(f"🔗 Conectando ao MLflow: {tracking_uri}")
    print(f"📦 Modelo: {model_name}")
    print(f"🆔 Version: {version}")

    #  promove o modelo para produção
    print(f"\n🚀 Promovendo modelo dev.{model_name}/{version} para produção...")
    result = client.copy_model_version(src_model_uri=f"models:/dev.{model_name}/{version}", dst_name=f"prod.{model_name}",
)
    print(f"✅ Modelo promovido! Versão de produção: {result.version}")

    # Cria um alias "champion" para a versão do nosso modelo de produção
    print(f"\n🏆 Definindo alias 'champion' para versão {result.version}...")
    client.set_registered_model_alias(f"prod.{model_name}", "champion", result.version)
    
    print(f"\n✨ Promoção concluída! Modelo prod.{model_name}@champion está pronto para uso.")

if __name__ == "__main__":
    # Configuração do argparse
    parser = argparse.ArgumentParser(description='Promote MLflow model from dev to prod')
    parser.add_argument('--model_name', help='Model name (e.g., mlops.kmeans-clustering). If not provided, reads from config/app_config.ini')
    parser.add_argument('--version', help='Model version. If not provided, reads from config/app_config.ini')
    args = parser.parse_args()
    
    # Se argumentos não foram fornecidos, lê do app_config.ini
    if args.model_name is None or args.version is None:
        config = configparser.ConfigParser()
        config_path = Path(__file__).parent.parent / "config" / "app_config.ini"
        config.read(config_path)
        
        model_name = args.model_name or config.get("ALL", "model_name")
        version = args.version or config.get("ALL", "current_version")
    else:
        model_name = args.model_name
        version = args.version
    
    main(model_name, version)

#python dist/promote_model.py
#python dist/promote_model.py --model_name mlops.kmeans-clustering --version 7