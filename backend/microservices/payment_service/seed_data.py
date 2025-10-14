# Script para popular banco de dados com dados de teste
# Útil para desenvolvimento e testes

import sys
from database import SessionLocal, create_tables
from models import Pagamento, FormaPagamento, StatusPagamento
from decimal import Decimal
from datetime import datetime, timedelta
import json


def seed_database():
    """Popula banco de dados com dados de teste"""
    
    print("🌱 Iniciando seed do banco de dados de pagamentos...")
    
    # Cria tabelas
    create_tables()
    
    # Cria sessão
    db = SessionLocal()
    
    try:
        # Verifica se já existem dados
        existing_pagamentos = db.query(Pagamento).count()
        if existing_pagamentos > 0:
            print(f"⚠️  Banco já possui {existing_pagamentos} pagamentos. Limpando...")
            db.query(Pagamento).delete()
            db.commit()
        
        # ==========================================
        # PAGAMENTOS
        # ==========================================
        
        print("\n💳 Criando pagamentos de exemplo...")
        
        pagamentos = [
            # Pagamentos aprovados com cartão
            Pagamento(
                usuario_id=1,
                pedido_id=1,
                forma_pagamento=FormaPagamento.CARTAO_CREDITO,
                status=StatusPagamento.APROVADO,
                valor=Decimal("149.90"),
                codigo_transacao="TXN-20251014-ABC12345",
                dados_pagamento=json.dumps({
                    "codigo_autorizacao": "123456",
                    "cartao_mascarado": "****-****-****-4242",
                    "parcelas": 3,
                    "valor_parcela": 49.97,
                    "bandeira": "Visa"
                }),
                data_processamento=datetime.now() - timedelta(days=5),
                data_aprovacao=datetime.now() - timedelta(days=5)
            ),
            Pagamento(
                usuario_id=2,
                pedido_id=2,
                forma_pagamento=FormaPagamento.CARTAO_CREDITO,
                status=StatusPagamento.APROVADO,
                valor=Decimal("89.90"),
                codigo_transacao="TXN-20251013-DEF67890",
                dados_pagamento=json.dumps({
                    "codigo_autorizacao": "654321",
                    "cartao_mascarado": "****-****-****-5555",
                    "parcelas": 1,
                    "valor_parcela": 89.90,
                    "bandeira": "Mastercard"
                }),
                data_processamento=datetime.now() - timedelta(days=3),
                data_aprovacao=datetime.now() - timedelta(days=3)
            ),
            
            # Pagamento PIX pendente
            Pagamento(
                usuario_id=3,
                pedido_id=3,
                forma_pagamento=FormaPagamento.PIX,
                status=StatusPagamento.PENDENTE,
                valor=Decimal("59.90"),
                codigo_transacao="TXN-20251014-GHI11111",
                dados_pagamento=json.dumps({
                    "chave_pix": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
                    "qr_code": "00020126580014br.gov.bcb.pix...",
                    "validade": (datetime.now() + timedelta(minutes=30)).isoformat(),
                    "status": "aguardando_pagamento"
                }),
                data_processamento=datetime.now() - timedelta(hours=1)
            ),
            
            # Pagamento PIX aprovado
            Pagamento(
                usuario_id=1,
                pedido_id=4,
                forma_pagamento=FormaPagamento.PIX,
                status=StatusPagamento.APROVADO,
                valor=Decimal("199.90"),
                codigo_transacao="TXN-20251012-JKL22222",
                dados_pagamento=json.dumps({
                    "chave_pix": "p6o5n4m3l2k1j0i9h8g7f6e5d4c3b2a1",
                    "qr_code": "00020126580014br.gov.bcb.pix...",
                    "status": "pago"
                }),
                data_processamento=datetime.now() - timedelta(days=2),
                data_aprovacao=datetime.now() - timedelta(days=2)
            ),
            
            # Pagamento Boleto pendente
            Pagamento(
                usuario_id=4,
                pedido_id=5,
                forma_pagamento=FormaPagamento.BOLETO,
                status=StatusPagamento.PENDENTE,
                valor=Decimal("299.90"),
                codigo_transacao="TXN-20251014-MNO33333",
                dados_pagamento=json.dumps({
                    "codigo_barras": "23790001192110001234567891234567890123456789",
                    "linha_digitavel": "23790.00119 21100.012345 67891.234567 8 90123456789",
                    "vencimento": (datetime.now() + timedelta(days=3)).isoformat(),
                    "nosso_numero": "00000005",
                    "banco": "237",
                    "status": "aguardando_pagamento"
                }),
                data_processamento=datetime.now() - timedelta(hours=3)
            ),
            
            # Pagamento Boleto aprovado
            Pagamento(
                usuario_id=2,
                pedido_id=6,
                forma_pagamento=FormaPagamento.BOLETO,
                status=StatusPagamento.APROVADO,
                valor=Decimal("179.90"),
                codigo_transacao="TXN-20251010-PQR44444",
                dados_pagamento=json.dumps({
                    "codigo_barras": "23790001192110001234567891234567890987654321",
                    "linha_digitavel": "23790.00119 21100.012345 67891.234567 8 90987654321",
                    "nosso_numero": "00000006",
                    "banco": "237",
                    "status": "pago"
                }),
                data_processamento=datetime.now() - timedelta(days=4),
                data_aprovacao=datetime.now() - timedelta(days=4)
            ),
            
            # Pagamento rejeitado
            Pagamento(
                usuario_id=5,
                pedido_id=7,
                forma_pagamento=FormaPagamento.CARTAO_CREDITO,
                status=StatusPagamento.REJEITADO,
                valor=Decimal("99.90"),
                codigo_transacao="TXN-20251014-STU55555",
                observacoes="Cartão recusado: Saldo insuficiente",
                data_processamento=datetime.now() - timedelta(hours=6)
            ),
            
            # Pagamento cancelado
            Pagamento(
                usuario_id=3,
                pedido_id=8,
                forma_pagamento=FormaPagamento.PIX,
                status=StatusPagamento.CANCELADO,
                valor=Decimal("129.90"),
                codigo_transacao="TXN-20251013-VWX66666",
                observacoes="Cancelado pelo usuário",
                data_processamento=datetime.now() - timedelta(days=1)
            ),
        ]
        
        db.add_all(pagamentos)
        db.commit()
        print(f"✅ Criados {len(pagamentos)} pagamentos")
        
        # ==========================================
        # RESUMO
        # ==========================================
        
        print("\n" + "=" * 60)
        print("✅ Seed concluído com sucesso!")
        print("=" * 60)
        print(f"💳 Pagamentos criados: {len(pagamentos)}")
        print("=" * 60)
        
        # Estatísticas
        aprovados = len([p for p in pagamentos if p.status == StatusPagamento.APROVADO])
        pendentes = len([p for p in pagamentos if p.status == StatusPagamento.PENDENTE])
        rejeitados = len([p for p in pagamentos if p.status == StatusPagamento.REJEITADO])
        cancelados = len([p for p in pagamentos if p.status == StatusPagamento.CANCELADO])
        
        print("\n📊 Estatísticas:")
        print(f"  ✅ Aprovados: {aprovados}")
        print(f"  ⏳ Pendentes: {pendentes}")
        print(f"  ❌ Rejeitados: {rejeitados}")
        print(f"  🚫 Cancelados: {cancelados}")
        
        print("\n📋 Exemplos de pagamentos:")
        for pag in pagamentos[:5]:
            print(f"  - ID {pag.id}: {pag.forma_pagamento.value} - R$ {pag.valor} - {pag.status.value}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro ao popular banco de dados: {str(e)}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
