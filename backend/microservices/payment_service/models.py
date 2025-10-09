# Modelos de dados para o microserviço de Pagamento
# Define as entidades Pagamento e enums FormaPagamento, StatusPagamento
# Implementa o modelo de domínio conforme diagrama UML

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum as SQLEnum, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()

class FormaPagamento(enum.Enum):
    CARTAO_CREDITO = "cartao_credito"
    CARTAO_DEBITO = "cartao_debito"
    PIX = "pix"
    BOLETO = "boleto"
    TRANSFERENCIA = "transferencia"

class StatusPagamento(enum.Enum):
    PENDENTE = "pendente"
    PROCESSANDO = "processando"
    APROVADO = "aprovado"
    REJEITADO = "rejeitado"
    CANCELADO = "cancelado"
    ESTORNADO = "estornado"

class Pagamento(Base):
    __tablename__ = "pagamentos"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False)  # Referência externa
    pedido_id = Column(Integer, nullable=False)  # Referência externa
    forma_pagamento = Column(SQLEnum(FormaPagamento), nullable=False)
    status = Column(SQLEnum(StatusPagamento), default=StatusPagamento.PENDENTE)
    valor = Column(Numeric(10, 2), nullable=False)
    codigo_transacao = Column(String(100), unique=True, index=True)
    dados_pagamento = Column(Text)  # JSON com dados específicos da forma de pagamento
    data_processamento = Column(DateTime)
    data_aprovacao = Column(DateTime)
    observacoes = Column(Text)
    data_criacao = Column(DateTime, default=func.now())
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relacionamentos (apenas dentro do mesmo microserviço)
    # Cross-service relationships são mantidos apenas via foreign keys