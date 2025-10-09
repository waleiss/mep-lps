#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de exemplo
Microserviço: Cart Service
"""

import sys
import os
from decimal import Decimal

# Adicionar o diretório atual ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
from models import Base, Carrinho, ItemCarrinho

def create_tables():
    """Criar todas as tabelas"""
    Base.metadata.create_all(bind=engine)

def seed_carrinhos():
    """Popular tabela de carrinhos com dados de exemplo"""
    db = SessionLocal()
    
    try:
        # Verificar se já existem carrinhos
        if db.query(Carrinho).count() > 0:
            print("Carrinhos já existem no banco. Pulando seed de carrinhos.")
            return
        
        # Nota: Em um cenário real, os carrinhos seriam criados dinamicamente
        # quando o usuário adiciona itens. Aqui criamos alguns exemplos.
        carrinhos_data = [
            {
                "usuario_id": 1,  # Assumindo que existe usuário com ID 1
                "ativo": True
            },
            {
                "usuario_id": 2,  # Assumindo que existe usuário com ID 2
                "ativo": True
            }
        ]
        
        for carrinho_data in carrinhos_data:
            carrinho = Carrinho(**carrinho_data)
            db.add(carrinho)
        
        db.commit()
        print(f"Criados {len(carrinhos_data)} carrinhos com sucesso!")
        
    except Exception as e:
        print(f"Erro ao criar carrinhos: {e}")
        db.rollback()
    finally:
        db.close()

def seed_itens_carrinho():
    """Popular tabela de itens do carrinho com dados de exemplo"""
    db = SessionLocal()
    
    try:
        # Verificar se já existem itens
        if db.query(ItemCarrinho).count() > 0:
            print("Itens de carrinho já existem no banco. Pulando seed de itens.")
            return
        
        itens_data = [
            {
                "carrinho_id": 1,
                "livro_id": 1,  # Assumindo que existe livro com ID 1
                "quantidade": 2,
                "preco_unitario": Decimal("45.90")
            },
            {
                "carrinho_id": 1,
                "livro_id": 2,  # Assumindo que existe livro com ID 2
                "quantidade": 1,
                "preco_unitario": Decimal("32.50")
            },
            {
                "carrinho_id": 2,
                "livro_id": 3,  # Assumindo que existe livro com ID 3
                "quantidade": 1,
                "preco_unitario": Decimal("39.90")
            }
        ]
        
        for item_data in itens_data:
            item = ItemCarrinho(**item_data)
            db.add(item)
        
        db.commit()
        print(f"Criados {len(itens_data)} itens de carrinho com sucesso!")
        
    except Exception as e:
        print(f"Erro ao criar itens de carrinho: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Função principal para executar o seed"""
    print("Iniciando seed do Cart Service...")
    
    # Criar tabelas
    print("Criando tabelas...")
    create_tables()
    
    # Popular dados
    print("Populando dados de carrinhos...")
    seed_carrinhos()
    
    print("Populando dados de itens de carrinho...")
    seed_itens_carrinho()
    
    print("Seed do Cart Service concluído com sucesso!")

if __name__ == "__main__":
    main()
