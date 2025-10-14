#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de exemplo
Microserviço: Shipping Service
"""

import sys
import os
from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Adicionar o diretório atual ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
from models import Base, Frete, TipoFrete, StatusFrete

def create_tables():
    """Criar todas as tabelas"""
    Base.metadata.create_all(bind=engine)

def seed_fretes():
    """Popular tabela de fretes com dados de exemplo"""
    db = SessionLocal()
    
    try:
        # Verificar se já existem fretes
        if db.query(Frete).count() > 0:
            print("Fretes já existem no banco. Pulando seed de fretes.")
            return
        
        fretes_data = [
            {
                "pedido_id": 1,
                "endereco_destino_id": 1,
                "tipo_frete": TipoFrete.PADRAO,
                "status": StatusFrete.EM_TRANSITO,
                "valor": Decimal("15.00"),
                "peso_total": Decimal("1.2"),
                "dimensoes": "20x15x5",
                "codigo_rastreamento": "BR123456789",
                "transportadora": "Correios",
                "prazo_entrega": 5,
                "observacoes": "Enviado via PAC",
                "data_coleta": datetime.now() - timedelta(days=2)
            },
            {
                "pedido_id": 2,
                "endereco_destino_id": 3,
                "tipo_frete": TipoFrete.EXPRESSO,
                "status": StatusFrete.ENTREGUE,
                "valor": Decimal("12.00"),
                "peso_total": Decimal("0.8"),
                "dimensoes": "18x12x3",
                "codigo_rastreamento": "BR987654321",
                "transportadora": "Correios",
                "prazo_entrega": 3,
                "observacoes": "Enviado via SEDEX",
                "data_coleta": datetime.now() - timedelta(days=3),
                "data_entrega": datetime.now() - timedelta(days=1)
            },
            {
                "pedido_id": 3,
                "endereco_destino_id": 2,
                "tipo_frete": TipoFrete.ECONOMICO,
                "status": StatusFrete.ENTREGUE,
                "valor": Decimal("18.00"),
                "peso_total": Decimal("2.1"),
                "dimensoes": "25x20x8",
                "codigo_rastreamento": "BR456789123",
                "transportadora": "Correios",
                "prazo_entrega": 7,
                "observacoes": "Enviado via PAC",
                "data_coleta": datetime.now() - timedelta(days=5),
                "data_entrega": datetime.now() - timedelta(days=2)
            }
        ]
        
        for frete_data in fretes_data:
            frete = Frete(**frete_data)
            db.add(frete)
        
        db.commit()
        print(f"Criados {len(fretes_data)} fretes com sucesso!")
        
    except Exception as e:
        print(f"Erro ao criar fretes: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Função principal para executar o seed"""
    print("Iniciando seed do Shipping Service...")
    
    # Criar tabelas
    print("Criando tabelas...")
    create_tables()
    
    # Popular dados
    print("Populando dados de fretes...")
    seed_fretes()
    
    print("Seed do Shipping Service concluído com sucesso!")

if __name__ == "__main__":
    main()
