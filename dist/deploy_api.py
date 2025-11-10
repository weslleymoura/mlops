from pathlib import Path
import sys 
current_path = Path(__file__).parent.resolve()
parent_path = current_path.parent.absolute()
sys.path.append(str(parent_path))

import os
import shutil
import argparse
import configparser
import logging
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main(version):
    
    # Diretório do deploy
    dir_source = './api'
    dir_deploy = './dist/api'
    dir_deploy_new_version = dir_deploy + '/{}'.format(version)
    dir_train = './temp'

    # Lista as versões atuais (já salvas do diretório)
    past_versions = next(os.walk(dir_deploy))[1]

    # Se já existe uma versão anterior, cancela o deploy
    try:
        if version in past_versions:
            raise ValueError('Não é possível gerar uma versão já existente.', 'versão', version)

        # Copia o source code para a pasta da nova versão
        shutil.copytree(dir_source, dir_deploy_new_version)

        # Limpa a pasta de artefatos do modelo
        shutil.rmtree(dir_deploy_new_version + '/model')

        # Copia os novos artefatos do modelo
        shutil.copytree(dir_train, dir_deploy_new_version + '/model')
        os.remove(dir_deploy_new_version + '/model/clustering_map.html')

        # Atualiza a versão no arquivo de configuração
        app_config = configparser.ConfigParser()
        app_config.read(dir_deploy_new_version + '/config/app_config.ini')
        app_config.set('PROD', 'version', version)
        app_config.set('DEV', 'version', version)
        app_config.set('PROD', 'model_location', 'model/clustering_model.joblib')
        app_config.set('DEV', 'model_location', 'model/clustering_model.joblib')
        app_config.set('PROD', 'sample_points_location', 'model/sample_points.joblib')
        app_config.set('DEV', 'sample_points_location', 'model/sample_points.joblib')

        with open(dir_deploy_new_version + '/config/app_config.ini', 'w') as configfile:
            app_config.write(configfile)

        # Copia requirements.txt
        shutil.copyfile('./requirements.txt', dir_deploy_new_version + '/requirements.txt')

        logger.info('Versão {} gerada com sucesso'.format(version))
    
    except ValueError as err:
        logger.error(err)
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Receive main parameters')
    parser.add_argument('--version', required=True, help='version')
    args = parser.parse_args()
    main(args.version)


    