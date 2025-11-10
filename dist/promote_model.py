from mlflow import MlflowClient
import mlflow
import argparse
from pathlib import Path
import os
import sys

def main(model_name, run_id):

    mlflow.set_tracking_uri("http://localhost:5000")
    client = MlflowClient()

    #  promove o modelo para produção
    result = client.copy_model_version(
        src_model_uri="models:/dev.{}@candidate-{}".format(model_name, run_id),
        dst_name="prod.{}".format(model_name),
    )

    # Cria um alias "champion" para a versão do nosso modelo de produção
    client.set_registered_model_alias("prod.{}".format(model_name), "champion", result.version)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Receive main parameters')
    parser.add_argument('--model_name', required=True, help='model name')
    parser.add_argument('--run_id', required=True, help='run id')
    args = parser.parse_args()
    main(args.model_name, args.run_id)