#!/usr/bin/env python3
"""
Script simples para manter o terminal/processo alive.
Útil para manter containers ou sessões ativas.
Pressione Ctrl+C para sair.
"""

import time
import datetime

def keep_alive():
    """Loop infinito que imprime timestamp a cada 60 segundos"""
    print("🟢 Keep-alive iniciado. Pressione Ctrl+C para sair.")
    print("-" * 50)
    
    counter = 0
    try:
        while True:
            counter += 1
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Alive - Iteração #{counter}")
            time.sleep(60)  # Aguarda 60 segundos
            
    except KeyboardInterrupt:
        print("\n" + "-" * 50)
        print("🔴 Keep-alive encerrado pelo usuário.")
        print(f"Total de iterações: {counter}")

if __name__ == "__main__":
    keep_alive()
