"""
Script para gerar traces de exemplo na API get_delivery_region
Chama a API 100 vezes usando pontos do sample_points.joblib
Configurado para 80% dentro da região e 20% fora
"""
import requests
import time
from joblib import load
import random
import numpy as np
from datetime import datetime

# Configurações
API_URL = "http://localhost:8000/get-delivery-region"
NUM_CALLS = 100
INSIDE_RATIO = 0.80  # 80% dentro da região
OUTSIDE_RATIO = 0.20  # 20% fora da região

# Carrega sample points
print("📦 Carregando sample_points.joblib...")
sample_points = load('temp/sample_points.joblib')

# sample_points é um dict com keys: 'covered' e 'not_covered'
inside_points = sample_points.get('covered', [])
outside_points = sample_points.get('not_covered', [])

print(f"✅ Carregados {len(inside_points)} pontos dentro da região")
print(f"❌ Carregados {len(outside_points)} pontos fora da região")

# Calcula quantas chamadas de cada tipo
num_inside = int(NUM_CALLS * INSIDE_RATIO)
num_outside = NUM_CALLS - num_inside

print(f"\n🎯 Configuração:")
print(f"  - Total de chamadas: {NUM_CALLS}")
print(f"  - Dentro da região: {num_inside} ({INSIDE_RATIO*100:.0f}%)")
print(f"  - Fora da região: {num_outside} ({OUTSIDE_RATIO*100:.0f}%)")

# Seleciona pontos aleatórios (com repetição para atingir NUM_CALLS)
selected_inside = random.choices(inside_points, k=num_inside)
selected_outside = random.choices(outside_points, k=num_outside)

# Combina e embaralha
all_points = selected_inside + selected_outside
random.shuffle(all_points)

# Adiciona variação nos pontos para simular drift realista
def add_noise(lat, lng, noise_level=0.001):
    """Adiciona pequena variação nas coordenadas"""
    lat_noise = random.uniform(-noise_level, noise_level)
    lng_noise = random.uniform(-noise_level, noise_level)
    return lat + lat_noise, lng + lng_noise

print(f"\n🚀 Iniciando chamadas à API...")
print(f"⏰ Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Contadores
success_count = 0
error_count = 0
inside_count = 0
outside_count = 0
total_time = 0

# Faz as chamadas
for i, point in enumerate(all_points, 1):
    lat = point['lat']
    lng = point['lng']
    
    # Adiciona pequena variação para simular dados reais
    lat_varied, lng_varied = add_noise(lat, lng)
    
    try:
        start_time = time.time()
        response = requests.get(f"{API_URL}/{lat_varied}/{lng_varied}", timeout=10)
        elapsed = time.time() - start_time
        total_time += elapsed
        
        if response.status_code == 200:
            result = response.json()
            success_count += 1
            
            # Conta dentro/fora
            if result.get('is_region_covered', False):
                inside_count += 1
                status = "✅ DENTRO"
            else:
                outside_count += 1
                status = "❌ FORA"
            
            print(f"[{i:3d}/{NUM_CALLS}] {status} | "
                  f"lat={lat_varied:.4f}, lng={lng_varied:.4f} | "
                  f"{elapsed*1000:.0f}ms | "
                  f"cluster={result.get('closest_center', {}).get('id', 'N/A')}")
        else:
            error_count += 1
            print(f"[{i:3d}/{NUM_CALLS}] ⚠️  ERRO {response.status_code}")
    
    except Exception as e:
        error_count += 1
        print(f"[{i:3d}/{NUM_CALLS}] ❌ ERRO: {str(e)}")
    
    # Pausa pequena entre requisições (opcional)
    time.sleep(0.1)

# Resumo final
print(f"\n{'='*70}")
print(f"📊 RESUMO DA EXECUÇÃO")
print(f"{'='*70}")
print(f"⏰ Fim: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"✅ Sucessos: {success_count}/{NUM_CALLS}")
print(f"❌ Erros: {error_count}/{NUM_CALLS}")
print(f"📍 Dentro da região: {inside_count} ({inside_count/success_count*100:.1f}%)")
print(f"📍 Fora da região: {outside_count} ({outside_count/success_count*100:.1f}%)")
print(f"⏱️  Tempo médio: {total_time/success_count*1000:.0f}ms" if success_count > 0 else "N/A")
print(f"⏱️  Tempo total: {total_time:.2f}s")
print(f"\n🔍 Traces disponíveis em: http://localhost:5000/#/traces")
print(f"📊 Dashboard: streamlit run dashboard/drift_monitor.py")
