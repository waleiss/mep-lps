# Modelos de dados para o microserviço de Frete
# Define as entidades Frete, Endereco e enums TipoFrete
# Implementa o modelo de domínio conforme diagrama UML

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum as SQLEnum, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()

class TipoFrete(enum.Enum):
    ECONOMICO = "economico"
    PADRAO = "padrao"
    EXPRESSO = "expresso"
    URGENTE = "urgente"

class StatusFrete(enum.Enum):
    PENDENTE = "pendente"
    COLETADO = "coletado"
    EM_TRANSITO = "em_transito"
    ENTREGUE = "entregue"
    DEVOLVIDO = "devolvido"
    CANCELADO = "cancelado"

class Endereco(Base):
    __tablename__ = "enderecos"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False, index=True)  # Referência externa ao serviço de usuários
    cep = Column(String(8), nullable=False)
    logradouro = Column(String(200), nullable=False)
    numero = Column(String(20), nullable=False)
    complemento = Column(String(100))
    bairro = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)
    apelido = Column(String(50))  # Ex: "Casa", "Trabalho", "Mãe"
    principal = Column(Boolean, default=False)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=func.now())
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())


class Frete(Base):
    __tablename__ = "fretes"
    
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, nullable=False)  # Referência externa
    endereco_destino_id = Column(Integer, nullable=False)  # Referência externa
    tipo_frete = Column(SQLEnum(TipoFrete), nullable=False)
    status = Column(SQLEnum(StatusFrete), default=StatusFrete.PENDENTE)
    valor = Column(Numeric(10, 2), nullable=False)
    peso_total = Column(Numeric(8, 3))  # em kg
    dimensoes = Column(String(100))  # formato: LxAxP
    codigo_rastreamento = Column(String(100), unique=True, index=True)
    transportadora = Column(String(100))
    prazo_entrega = Column(Integer)  # em dias
    observacoes = Column(Text)
    data_coleta = Column(DateTime)
    data_entrega = Column(DateTime)
    data_criacao = Column(DateTime, default=func.now())
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relacionamentos (apenas dentro do mesmo microserviço)
    # Cross-service relationships são mantidos apenas via foreign keys