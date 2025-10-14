#!/usr/bin/env python3
"""
Script principal para popular todos os microserviços com dados de exemplo
"""

import subprocess
import sys
import os

def run_seed(service_name, service_path):
    """Executa o script de seed de um microserviço"""
    print(f"\n{'='*50}")
    print(f"Executando seed do {service_name}")
    print(f"{'='*50}")
    
    try:
        # Mudar para o diretório do serviço
        original_dir = os.getcwd()
        os.chdir(service_path)
        
        # Executar o script de seed
        result = subprocess.run([sys.executable, "seed_data.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"[OK] Seed do {service_name} executado com sucesso!")
            print(result.stdout)
        else:
            print(f"[ERRO] Erro ao executar seed do {service_name}:")
            print(result.stderr)
            
    except Exception as e:
        print(f"[ERRO] Erro inesperado no seed do {service_name}: {e}")
    finally:
        # Voltar ao diretório original
        os.chdir(original_dir)

def main():
    """Função principal"""
    print("Iniciando seed de todos os microserviços...")
    
    # Definir os microserviços e seus caminhos
    services = [
        ("Auth Service", "microservices/auth_service"),
        ("Catalog Service", "microservices/catalog_service"),
        ("Cart Service", "microservices/cart_service"),
        ("Order Service", "microservices/order_service"),
        ("Payment Service", "microservices/payment_service"),
        ("Shipping Service", "microservices/shipping_service"),
        ("Recommendation Service", "microservices/recommendation_service")
    ]
    
    # Executar seed de cada serviço
    for service_name, service_path in services:
        run_seed(service_name, service_path)
    
    print(f"\n{'='*50}")
    print("Seed de todos os microserviços concluído!")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
