import folium
import random 
from pathlib import Path
import json
import numpy as np
import geopy.distance
import configparser

# Vamos criar uma função para exibir uma instância de entrega no mapa
def plot_points(points, markers):

    # Cria um mapa
    m = folium.Map(
        location=(points[0]['lat'], points[0]['lng']),
        zoom_start=12,
        tiles="OpenStreetMap",
    )

    # Adiciona um feature group para colocarmos os pins no mapa
    fg_points = folium.FeatureGroup(name='Points').add_to(m)

    # Adiciona pontos ao mapa
    for point in points:
        folium.CircleMarker(
            [point['lat'], point['lng']], color=point['color'], radius=1, weight=1, popup="Cluster: {} | Dist: {}".format(point['cluster'], point['dist']) 
        ).add_to(m)

    # Adiciona marcadores ao mapa
    if markers != None:
        for marker in markers:

            # Adiciona os marcadores do tipo pin no mapa
            if 'pin' in (marker['type']):
                folium_marker = folium.Marker(location=[marker['lat'], marker['lng']], radius=10, tooltip=marker['tooltip'], icon=folium.Icon(color=marker['color']))
                folium_marker.add_to(fg_points)
            
            # Adiciona os marcadores do tipo cluster no mapa
            if 'cluster' in (marker['type']):
                folium.Circle([marker['lat'], marker['lng']], color=marker['color'], radius=5000, weight=3, popup="5 km").add_to(m)

    # Adiciona legenda ao mapa
    m.add_child(folium.LayerControl(position='topright', collapsed=False, autoZIndex=True))

    return m

# Função que recebe uma instância de entrega e retorna uma lista de pontos (lat, lng)
def get_delivery_coordinates(instance):
    
    points = []
    for delivery in instance['deliveries']:
        points.append(delivery['point'])

    return points

# Cria uma função para gerar cores aleatórias
get_colors = lambda n: ["#%06x" % random.randint(0, 0xFFFFFF) for _ in range(n)]


def load_training_data(path_str):

    # Converte o nome da pasta em uma variável `Path`
    path = Path(path_str)

    # Passa por todos os arquivos da pasta e carrega os dados em `instances`
    instances = []
    for file in path.iterdir():

        # Acessa o arquivo
        with open(file) as f:

            # Lê os dados do arquivo
            data = json.load(f)

        # Adiciona os dados do arquivo à lista `instances`
        instances.append(data)

    print ("Foram carregados {} arquivos".format(len(instances)))
    print ("O objeto instances é do tipo {}".format(type(instances)))

    return instances

def prepare_points(instances):

    # Junta todos os pontos de entrega de todas as instâncias em uma única lista
    points = []
    for instance in instances:
        points.extend(get_delivery_coordinates(instance))

    # Adiciona a cor de cada ponto
    for p in points:
        p['color'] = 'blue'
        p['cluster'] = None
        p['dist'] = None

    # Preparando os dados para o modelo de clustering
    input_points = [ (p['lat'], p['lng']) for p in points]
    input_points = np.array(input_points)

    return points

def prepare_input_points(points):

    # Preparando os dados para o modelo de clustering
    input_points = [ (p['lat'], p['lng']) for p in points]
    input_points = np.array(input_points)

    return input_points


def add_clusters_to_markers(model):

    # Adiciona o centróide de cada cluster como um marcador no mapa
    markers = []
    for i, center in enumerate(model.cluster_centers_):
        m = dict()
        m['lat'] = center[0]
        m['lng'] = center[1]
        m['cluster'] = i
        m['color'] = 'black'
        m['type'] = ['cluster', 'pin']
        m['tooltip'] = 'Cluster {}'.format(i)
        markers.append(m)
        
    return markers

def enrich_points_with_cluster_info(points, model, markers, cm):

    # Preparando os pontos do mapa
    for p in points:
        cluster = model.predict([[ p['lat'], p['lng'] ]] )
        c = cluster[0]
        p['cluster'] = c
        p['color'] = cm[c]

        # Calcula a distância do ponto para o seu cluster
        coord_p = (p['lat'], p['lng'])
        coord_cluster = (markers[c]['lat'], markers[c]['lng'])
        p['dist'] = geopy.distance.geodesic(coord_p, coord_cluster).km

    return points



def generate_sample_points(points, markers):

    sample_points = dict()
    sample_points['covered'] = []
    sample_points['not_covered'] = []

    for p in points:
        coords_p = (p['lat'], p['lng'])
        coords_p_dict = {
            'lat': p['lat'],
            'lng': p['lng']
        }

        # Verifica a distância (em km) entre o ponto a cada cluster
        res = dict()
        for m in markers:
            coords_cluster = (m['lat'], m['lng'])
            res[m['cluster']] = geopy.distance.geodesic(coords_cluster, coords_p).km

        # Cria uma lista com as chaves (keys) ordenadas pelos seus valores (values)
        res_sorted_keys = sorted(res, key=res.get, reverse=False)

        # Busca a distância mais curta
        dist = round(res[res_sorted_keys[0]], 2)

        if (dist <= 5 and len(sample_points['covered']) < 10):
            sample_points['covered'] += [coords_p_dict]
        elif (dist > 5 and len(sample_points['not_covered']) < 10):
            sample_points['not_covered'] += [coords_p_dict]

        if len(sample_points['covered']) + len(sample_points['not_covered']) == 20:
            break

    return sample_points


def add_sample_points_to_markers (markers, sample_points):

    # Prepara um novo marcador para incluir os novos pontos
    markers_test = markers.copy()

    for sample in sample_points['covered']:
        new_entry = {
            'lat': sample['lat'],  
            'lng': sample['lng'],
            'cluster': None,
            'color': 'blue',
            'type': ['pin'],
            'tooltip': 'Ponto de exemplo dentro da região de entrega'
        }

        markers_test.append(new_entry)

    for sample in sample_points['not_covered']:
        new_entry = {
            'lat': sample['lat'],  
            'lng': sample['lng'],
            'cluster': None,
            'color': 'red',
            'type': ['pin'],
            'tooltip': 'Ponto de exemplo fora da região de entrega'
        }

        markers_test.append(new_entry)
        
    return markers_test


def get_drift_params(distances):

    drift_params = dict()
    for k, v in distances.items():

        # Percorre cada ponto de treino para calcular outliers and inner_radius
        outliers = []
        inner_radius = []
        for x in v:
            z_score = (x - np.mean(v)) / np.std(v)
            outliers += [z_score >= 2]
            inner_radius += [x <= 5]
            

        # Cataloga as informações de drift para o cluster
        drift_params[k] = {
            'mean': round(np.mean(v), 2),
            'stdev': round(np.std(v), 2),
            'perc_outliers': round(sum(outliers) / len(outliers), 4),
            'perc_inner_radius': round(sum(inner_radius) / len(inner_radius), 4)
        }
    
    return drift_params

def update_app_config(filename, values):
    
    # Read the existing configuration file
    config = configparser.ConfigParser()
    config.read(filename)

    # Append new settings
    for k, v in values.items():
        config['ALL'][k] = v

    # Write the updated configuration back to the file
    with open(filename, 'w') as configfile:
        config.write(configfile)

def load_requirements(file_path):
    
    with open(file_path, 'r') as file:
        requirements = file.read().splitlines()
    return requirements