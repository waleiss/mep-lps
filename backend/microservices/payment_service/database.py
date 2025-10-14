# Configuração do banco de dados PostgreSQL para pagamentos
# Conexão com Banco de Dados 5 Pagamentos
# Implementa RNF2.1, RNF2.2 para segurança

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Configuração do banco de dados
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://admin:admin1234@localhost:5436/mundo_palavras_payments"
)

# Criar engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Criar sessão do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()

# Função para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para criar tabelas
def create_tables():
    from models import Base
    Base.metadata.create_all(bind=engine)