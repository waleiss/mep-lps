# Modelos de dados para o microserviço de Pedidos
# Define as entidades Pedido, ItemPedido e enums StatusPedido
# Implementa o modelo de domínio conforme diagrama UML

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum as SQLEnum, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()

class StatusPedido(enum.Enum):
    PENDENTE = "pendente"
    CONFIRMADO = "confirmado"
    PROCESSANDO = "processando"
    ENVIADO = "enviado"
    ENTREGUE = "entregue"
    CANCELADO = "cancelado"
    DEVOLVIDO = "devolvido"

class Pedido(Base):
    __tablename__ = "pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False)  # Referência externa
    endereco_entrega_id = Column(Integer, nullable=False)  # Referência externa
    numero_pedido = Column(String(50), unique=True, index=True, nullable=False)
    status = Column(SQLEnum(StatusPedido), default=StatusPedido.PENDENTE)
    valor_total = Column(Numeric(10, 2), nullable=False)
    valor_frete = Column(Numeric(10, 2), default=0)
    observacoes = Column(Text)
    data_criacao = Column(DateTime, default=func.now())
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())
    data_entrega_prevista = Column(DateTime)
    data_entrega_realizada = Column(DateTime)
    
    # Relacionamentos (apenas dentro do mesmo microserviço)
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")

class ItemPedido(Base):
    __tablename__ = "itens_pedido"
    
    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    livro_id = Column(Integer, nullable=False)  # Referência externa
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    data_criacao = Column(DateTime, default=func.now())
    
    # Relacionamentos (apenas dentro do mesmo microserviço)
    pedido = relationship("Pedido", back_populates="itens")
    
    @property
    def subtotal(self):
        return self.preco_unitario * self.quantidade