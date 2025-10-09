# Modelos de dados para o microserviço de Recomendação
# Define as entidades Recomendacao e enums TipoRecomendacao
# Implementa o modelo de domínio conforme diagrama UML

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum as SQLEnum, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()

class TipoRecomendacao(enum.Enum):
    BASEADA_USUARIO = "baseada_usuario"
    BASEADA_ITEM = "baseada_item"
    COLABORATIVA = "colaborativa"
    CONTEUDO = "conteudo"
    HIBRIDA = "hibrida"

class StatusRecomendacao(enum.Enum):
    ATIVA = "ativa"
    INATIVA = "inativa"
    EXCLUIDA = "excluida"

class Recomendacao(Base):
    __tablename__ = "recomendacoes"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False)  # Referência externa
    livro_id = Column(Integer, nullable=False)  # Referência externa
    tipo = Column(SQLEnum(TipoRecomendacao), nullable=False)
    status = Column(SQLEnum(StatusRecomendacao), default=StatusRecomendacao.ATIVA)
    score = Column(Numeric(5, 4))  # pontuação de 0 a 1
    algoritmo = Column(String(100))  # nome do algoritmo usado
    parametros = Column(Text)  # JSON com parâmetros do algoritmo
    data_criacao = Column(DateTime, default=func.now())
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())
    data_expiracao = Column(DateTime)
    
    # Relacionamentos (apenas dentro do mesmo microserviço)
    # Cross-service relationships são mantidos apenas via foreign keys