# Configuração do banco de dados PostgreSQL para carrinho
# Conexão com Banco de Dados 3 Carrinho e Redis Cache
# Implementa RNF1.1 para performance

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# Configuração do banco de dados PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", settings.database_url)

# Criar engine do SQLAlchemy
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.debug
)

# Criar sessão do banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos
Base = declarative_base()


# Função para obter sessão do banco
def get_db():
    """
    Dependency for getting database session
    
    Yields:
        Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Função para criar tabelas
def create_tables():
    """Create all database tables"""
    from models import Base
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")