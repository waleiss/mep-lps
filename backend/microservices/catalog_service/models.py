# Modelos de dados para o microserviço de Catálogo
# Define as entidades Livro, CondicaoLivro e enums relacionados
# Implementa o modelo de domínio conforme diagrama UML

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum as SQLEnum, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()

class CondicaoLivro(enum.Enum):
    NOVO = "novo"
    USADO = "usado"
    SEMI_NOVO = "semi_novo"

class Categoria(enum.Enum):
    FICCAO = "ficcao"
    NAO_FICCAO = "nao_ficcao"
    TECNICO = "tecnico"
    ACADEMICO = "academico"
    INFANTIL = "infantil"
    OUTROS = "outros"

class Livro(Base):
    __tablename__ = "livros"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    autor = Column(String(255), nullable=False)
    isbn = Column(String(13), unique=True, index=True)
    editora = Column(String(100))
    ano_publicacao = Column(Integer)
    edicao = Column(String(50))
    numero_paginas = Column(Integer)
    sinopse = Column(Text)
    preco = Column(Numeric(10, 2), nullable=False)
    estoque = Column(Integer, default=0)
    categoria = Column(SQLEnum(Categoria), default=Categoria.OUTROS)
    condicao = Column(SQLEnum(CondicaoLivro), default=CondicaoLivro.NOVO)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=func.now())
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relacionamentos (apenas dentro do mesmo microserviço)
    # Cross-service relationships são mantidos apenas via foreign keys