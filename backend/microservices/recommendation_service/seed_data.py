#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de exemplo
Microserviço: Recommendation Service
"""

import sys
import os
from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Adicionar o diretório atual ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal, engine
from models import Base, Recomendacao, TipoRecomendacao, StatusRecomendacao

def create_tables():
    """Criar todas as tabelas"""
    Base.metadata.create_all(bind=engine)

def seed_recomendacoes():
    """Popular tabela de recomendações com dados de exemplo"""
    db = SessionLocal()
    
    try:
        # Verificar se já existem recomendações
        if db.query(Recomendacao).count() > 0:
            print("Recomendações já existem no banco. Pulando seed de recomendações.")
            return
        
        recomendacoes_data = [
            {
                "usuario_id": 1,
                "livro_id": 3,
                "tipo": TipoRecomendacao.COLABORATIVA,
                "status": StatusRecomendacao.ATIVA,
                "score": Decimal("0.85"),
                "algoritmo": "collaborative_filtering",
                "parametros": '{"min_similarity": 0.7, "neighbors": 10}',
                "data_expiracao": datetime.now() + timedelta(days=30)
            },
            {
                "usuario_id": 1,
                "livro_id": 4,
                "tipo": TipoRecomendacao.CONTEUDO,
                "status": StatusRecomendacao.ATIVA,
                "score": Decimal("0.72"),
                "algoritmo": "content_based",
                "parametros": '{"similarity_threshold": 0.6, "features": ["categoria", "autor"]}',
                "data_expiracao": datetime.now() + timedelta(days=30)
            },
            {
                "usuario_id": 2,
                "livro_id": 1,
                "tipo": TipoRecomendacao.HIBRIDA,
                "status": StatusRecomendacao.ATIVA,
                "score": Decimal("0.91"),
                "algoritmo": "hybrid_recommender",
                "parametros": '{"collaborative_weight": 0.6, "content_weight": 0.4}',
                "data_expiracao": datetime.now() + timedelta(days=30)
            },
            {
                "usuario_id": 2,
                "livro_id": 5,
                "tipo": TipoRecomendacao.BASEADA_USUARIO,
                "status": StatusRecomendacao.ATIVA,
                "score": Decimal("0.68"),
                "algoritmo": "user_based_cf",
                "parametros": '{"min_ratings": 5, "similarity_metric": "cosine"}',
                "data_expiracao": datetime.now() + timedelta(days=30)
            },
            {
                "usuario_id": 1,
                "livro_id": 6,
                "tipo": TipoRecomendacao.BASEADA_ITEM,
                "status": StatusRecomendacao.ATIVA,
                "score": Decimal("0.74"),
                "algoritmo": "item_based_cf",
                "parametros": '{"min_common_users": 3, "similarity_threshold": 0.5}',
                "data_expiracao": datetime.now() + timedelta(days=30)
            }
        ]
        
        for recomendacao_data in recomendacoes_data:
            recomendacao = Recomendacao(**recomendacao_data)
            db.add(recomendacao)
        
        db.commit()
        print(f"Criadas {len(recomendacoes_data)} recomendações com sucesso!")
        
    except Exception as e:
        print(f"Erro ao criar recomendações: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Função principal para executar o seed"""
    print("Iniciando seed do Recommendation Service...")
    
    # Criar tabelas
    print("Criando tabelas...")
    create_tables()
    
    # Popular dados
    print("Populando dados de recomendações...")
    seed_recomendacoes()
    
    print("Seed do Recommendation Service concluído com sucesso!")

if __name__ == "__main__":
    main()
