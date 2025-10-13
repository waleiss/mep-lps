#!/usr/bin/env python3
"""
Script de teste rápido para o Cart Service
Valida os principais endpoints e funcionalidades
"""

import requests
import json
from decimal import Decimal

BASE_URL = "http://localhost:8003/api/v1"
USER_ID = 1


def print_response(title, response):
    """Imprime resposta formatada"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"Error: {response.text}")
    print(f"{'='*60}\n")


def test_health_check():
    """Testa health check"""
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    return response.status_code == 200


def test_get_cart():
    """Testa obter carrinho"""
    response = requests.get(f"{BASE_URL}/carrinho/{USER_ID}")
    print_response("Obter Carrinho", response)
    return response.status_code == 200


def test_add_item():
    """Testa adicionar item"""
    data = {
        "livro_id": 101,
        "quantidade": 2
    }
    response = requests.post(
        f"{BASE_URL}/carrinho/{USER_ID}/add",
        json=data
    )
    print_response("Adicionar Item", response)
    return response.status_code == 200


def test_add_another_item():
    """Testa adicionar outro item"""
    data = {
        "livro_id": 102,
        "quantidade": 1
    }
    response = requests.post(
        f"{BASE_URL}/carrinho/{USER_ID}/add",
        json=data
    )
    print_response("Adicionar Outro Item", response)
    return response.status_code == 200


def test_update_quantity():
    """Testa atualizar quantidade"""
    data = {
        "quantidade": 5
    }
    response = requests.put(
        f"{BASE_URL}/carrinho/{USER_ID}/update/101",
        json=data
    )
    print_response("Atualizar Quantidade", response)
    return response.status_code == 200


def test_remove_item():
    """Testa remover item"""
    response = requests.delete(
        f"{BASE_URL}/carrinho/{USER_ID}/remove/102"
    )
    print_response("Remover Item", response)
    return response.status_code == 200


def test_clear_cart():
    """Testa limpar carrinho"""
    response = requests.delete(
        f"{BASE_URL}/carrinho/{USER_ID}/clear"
    )
    print_response("Limpar Carrinho", response)
    return response.status_code == 200


def run_all_tests():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("  INICIANDO TESTES DO CART SERVICE")
    print("="*60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Obter Carrinho (vazio)", test_get_cart),
        ("Adicionar Item 1", test_add_item),
        ("Adicionar Item 2", test_add_another_item),
        ("Visualizar Carrinho (com itens)", test_get_cart),
        ("Atualizar Quantidade", test_update_quantity),
        ("Visualizar Carrinho (após update)", test_get_cart),
        ("Remover Item", test_remove_item),
        ("Visualizar Carrinho (após remoção)", test_get_cart),
        ("Limpar Carrinho", test_clear_cart),
        ("Visualizar Carrinho (após limpar)", test_get_cart),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"\n❌ Erro ao executar {test_name}: {str(e)}\n")
            results.append((test_name, False))
    
    # Resultado final
    print("\n" + "="*60)
    print("  RESULTADOS DOS TESTES")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{status} - {test_name}")
    
    print(f"\n{'='*60}")
    print(f"  Total: {passed}/{total} testes passaram")
    print(f"{'='*60}\n")
    
    if passed == total:
        print("🎉 TODOS OS TESTES PASSARAM! 🎉\n")
    else:
        print(f"⚠️  {total - passed} teste(s) falharam\n")


if __name__ == "__main__":
    print("\n⚠️  ATENÇÃO: Certifique-se de que o Cart Service está rodando!")
    print("   Execute: uvicorn main:app --reload --port 8003\n")
    
    input("Pressione ENTER para começar os testes...")
    
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: Não foi possível conectar ao Cart Service")
        print("   Verifique se o serviço está rodando em http://localhost:8003\n")
    except KeyboardInterrupt:
        print("\n\n⚠️  Testes interrompidos pelo usuário\n")
