#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de exemplo
Microserviço: Order Service
"""

import sys
import os
from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Adicionar o diretório atual ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
from models import Base, Pedido, ItemPedido, StatusPedido

def create_tables():
    """Criar todas as tabelas"""
    Base.metadata.create_all(bind=engine)

def seed_pedidos():
    """Popular tabela de pedidos com dados de exemplo"""
    db = SessionLocal()
    
    try:
        # Verificar se já existem pedidos
        if db.query(Pedido).count() > 0:
            print("Pedidos já existem no banco. Pulando seed de pedidos.")
            return
        
        pedidos_data = [
            {
                "usuario_id": 1,
                "endereco_entrega_id": 1,
                "numero_pedido": "PED-001-2024",
                "status": StatusPedido.CONFIRMADO,
                "valor_total": Decimal("124.30"),
                "valor_frete": Decimal("15.00"),
                "observacoes": "Entregar no período da manhã",
                "data_entrega_prevista": datetime.now() + timedelta(days=5)
            },
            {
                "usuario_id": 2,
                "endereco_entrega_id": 3,
                "numero_pedido": "PED-002-2024",
                "status": StatusPedido.ENVIADO,
                "valor_total": Decimal("39.90"),
                "valor_frete": Decimal("12.00"),
                "observacoes": "",
                "data_entrega_prevista": datetime.now() + timedelta(days=3)
            },
            {
                "usuario_id": 1,
                "endereco_entrega_id": 2,
                "numero_pedido": "PED-003-2024",
                "status": StatusPedido.ENTREGUE,
                "valor_total": Decimal("89.90"),
                "valor_frete": Decimal("18.00"),
                "observacoes": "Entregue com sucesso",
                "data_entrega_prevista": datetime.now() - timedelta(days=2),
                "data_entrega_realizada": datetime.now() - timedelta(days=1)
            }
        ]
        
        for pedido_data in pedidos_data:
            pedido = Pedido(**pedido_data)
            db.add(pedido)
        
        db.commit()
        print(f"Criados {len(pedidos_data)} pedidos com sucesso!")
        
    except Exception as e:
        print(f"Erro ao criar pedidos: {e}")
        db.rollback()
    finally:
        db.close()

def seed_itens_pedido():
    """Popular tabela de itens do pedido com dados de exemplo"""
    db = SessionLocal()
    
    try:
        # Verificar se já existem itens
        if db.query(ItemPedido).count() > 0:
            print("Itens de pedido já existem no banco. Pulando seed de itens.")
            return
        
        itens_data = [
            {
                "pedido_id": 1,
                "livro_id": 1,
                "quantidade": 2,
                "preco_unitario": Decimal("45.90")
            },
            {
                "pedido_id": 1,
                "livro_id": 2,
                "quantidade": 1,
                "preco_unitario": Decimal("32.50")
            },
            {
                "pedido_id": 2,
                "livro_id": 3,
                "quantidade": 1,
                "preco_unitario": Decimal("39.90")
            },
            {
                "pedido_id": 3,
                "livro_id": 4,
                "quantidade": 1,
                "preco_unitario": Decimal("89.90")
            }
        ]
        
        for item_data in itens_data:
            item = ItemPedido(**item_data)
            db.add(item)
        
        db.commit()
        print(f"Criados {len(itens_data)} itens de pedido com sucesso!")
        
    except Exception as e:
        print(f"Erro ao criar itens de pedido: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Função principal para executar o seed"""
    print("Iniciando seed do Order Service...")
    
    # Criar tabelas
    print("Criando tabelas...")
    create_tables()
    
    # Popular dados
    print("Populando dados de pedidos...")
    seed_pedidos()
    
    print("Populando dados de itens de pedido...")
    seed_itens_pedido()
    
    print("Seed do Order Service concluído com sucesso!")

if __name__ == "__main__":
    main()
