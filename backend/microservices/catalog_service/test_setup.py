#!/usr/bin/env python3
"""
Script de teste para verificar funcionamento do Catalog Service
"""

import sys
import os

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Testar se todos os módulos podem ser importados"""
    print("Testando imports...")
    
    try:
        from config import settings
        print("✓ config.py - OK")
        
        from database import engine, get_db, create_tables
        print("✓ database.py - OK")
        
        from models import Livro, Categoria, CondicaoLivro
        print("✓ models.py - OK")
        
        from repositories.book_repository import BookRepository
        print("✓ repositories/book_repository.py - OK")
        
        from services.cache_service import cache_service
        print("✓ services/cache_service.py - OK")
        
        from services.book_service import BookService
        print("✓ services/book_service.py - OK")
        
        from schemas.book_schemas import BookCreate, BookUpdate, BookResponse
        print("✓ schemas/book_schemas.py - OK")
        
        from routes import router
        print("✓ routes.py - OK")
        
        from main import app
        print("✓ main.py - OK")
        
        print("\n✅ Todos os imports funcionaram corretamente!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao importar: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_connection():
    """Testar conexão com o banco de dados"""
    print("\nTestando conexão com banco de dados...")
    
    try:
        from database import engine
        
        # Tentar conectar
        with engine.connect() as conn:
            print("✓ Conexão com banco de dados - OK")
            return True
            
    except Exception as e:
        print(f"⚠ Aviso: Não foi possível conectar ao banco de dados: {e}")
        print("  Certifique-se de que o PostgreSQL está rodando.")
        return False

def test_cache_connection():
    """Testar conexão com Redis"""
    print("\nTestando conexão com Redis...")
    
    try:
        from services.cache_service import cache_service
        
        if cache_service.is_available():
            print("✓ Conexão com Redis - OK")
            return True
        else:
            print("⚠ Aviso: Redis não está disponível")
            print("  Cache estará desabilitado mas o serviço funcionará.")
            return False
            
    except Exception as e:
        print(f"⚠ Aviso: Erro ao conectar com Redis: {e}")
        return False

def test_database_tables():
    """Testar criação de tabelas"""
    print("\nTestando criação de tabelas...")
    
    try:
        from database import create_tables
        
        create_tables()
        print("✓ Tabelas criadas/verificadas - OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar tabelas: {e}")
        return False

def main():
    """Executar todos os testes"""
    print("=" * 60)
    print("Teste do Catalog Service")
    print("=" * 60)
    
    results = []
    
    # Teste 1: Imports
    results.append(("Imports", test_imports()))
    
    # Teste 2: Conexão com banco
    results.append(("Database Connection", test_database_connection()))
    
    # Teste 3: Conexão com Redis
    results.append(("Redis Connection", test_cache_connection()))
    
    # Teste 4: Criação de tabelas
    results.append(("Database Tables", test_database_tables()))
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    
    for name, success in results:
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"{name:.<40} {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\nTotal: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 Todos os testes passaram! O serviço está pronto para uso.")
        print("\nPróximos passos:")
        print("1. Execute: python seed_data.py (para popular o banco)")
        print("2. Execute: uvicorn main:app --reload --port 8002")
        print("3. Acesse: http://localhost:8002/docs")
    else:
        print("\n⚠ Alguns testes falharam. Verifique as mensagens acima.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
