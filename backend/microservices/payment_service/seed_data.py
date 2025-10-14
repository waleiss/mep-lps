#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de exemplo
Microserviço: Payment Service
"""

import sys
import os
from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Adicionar o diretório atual ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
from models import Base, Pagamento, FormaPagamento, StatusPagamento

def create_tables():
    """Criar todas as tabelas"""
    Base.metadata.create_all(bind=engine)

def seed_pagamentos():
    """Popular tabela de pagamentos com dados de exemplo"""
    db = SessionLocal()
    
    try:
        # Verificar se já existem pagamentos
        if db.query(Pagamento).count() > 0:
            print("Pagamentos já existem no banco. Pulando seed de pagamentos.")
            return
        
        pagamentos_data = [
            {
                "usuario_id": 1,
                "pedido_id": 1,
                "forma_pagamento": FormaPagamento.CARTAO_CREDITO,
                "status": StatusPagamento.APROVADO,
                "valor": Decimal("124.30"),
                "codigo_transacao": "TXN-001-2024-ABC123",
                "dados_pagamento": '{"ultimos_digitos": "1234", "bandeira": "Visa"}',
                "data_processamento": datetime.now() - timedelta(hours=2),
                "data_aprovacao": datetime.now() - timedelta(hours=1),
                "observacoes": "Pagamento aprovado com sucesso"
            },
            {
                "usuario_id": 2,
                "pedido_id": 2,
                "forma_pagamento": FormaPagamento.PIX,
                "status": StatusPagamento.APROVADO,
                "valor": Decimal("39.90"),
                "codigo_transacao": "PIX-002-2024-DEF456",
                "dados_pagamento": '{"chave_pix": "usuario@email.com", "banco": "001"}',
                "data_processamento": datetime.now() - timedelta(hours=1),
                "data_aprovacao": datetime.now() - timedelta(minutes=30),
                "observacoes": "PIX processado instantaneamente"
            },
            {
                "usuario_id": 1,
                "pedido_id": 3,
                "forma_pagamento": FormaPagamento.CARTAO_DEBITO,
                "status": StatusPagamento.APROVADO,
                "valor": Decimal("89.90"),
                "codigo_transacao": "TXN-003-2024-GHI789",
                "dados_pagamento": '{"ultimos_digitos": "5678", "bandeira": "Mastercard"}',
                "data_processamento": datetime.now() - timedelta(days=1),
                "data_aprovacao": datetime.now() - timedelta(days=1),
                "observacoes": "Pagamento aprovado"
            }
        ]
        
        for pagamento_data in pagamentos_data:
            pagamento = Pagamento(**pagamento_data)
            db.add(pagamento)
        
        db.commit()
        print(f"Criados {len(pagamentos_data)} pagamentos com sucesso!")
        
    except Exception as e:
        print(f"Erro ao criar pagamentos: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Função principal para executar o seed"""
    print("Iniciando seed do Payment Service...")
    
    # Criar tabelas
    print("Criando tabelas...")
    create_tables()
    
    # Popular dados
    print("Populando dados de pagamentos...")
    seed_pagamentos()
    
    print("Seed do Payment Service concluído com sucesso!")

if __name__ == "__main__":
    main()
