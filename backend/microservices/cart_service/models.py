# Modelos de dados para o microserviço de Carrinho
# Define as entidades Carrinho, ItemCarrinho e cálculos
# Implementa o modelo de domínio conforme diagrama UML

from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


Base = declarative_base()

class Carrinho(Base):
    __tablename__ = "carrinhos"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, nullable=False)  # Referência externa
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=func.now())
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relacionamentos (apenas dentro do mesmo microserviço)
    itens = relationship("ItemCarrinho", back_populates="carrinho", cascade="all, delete-orphan")
    
    @property
    def total_itens(self):
        return sum(item.quantidade for item in self.itens)
    
    @property
    def valor_total(self):
        return sum(item.preco_unitario * item.quantidade for item in self.itens)

class ItemCarrinho(Base):
    __tablename__ = "itens_carrinho"
    
    id = Column(Integer, primary_key=True, index=True)
    carrinho_id = Column(Integer, ForeignKey("carrinhos.id"), nullable=False)
    livro_id = Column(Integer, nullable=False)  # Referência externa
    quantidade = Column(Integer, nullable=False, default=1)
    preco_unitario = Column(Numeric(10, 2), nullable=False)
    data_criacao = Column(DateTime, default=func.now())
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relacionamentos (apenas dentro do mesmo microserviço)
    carrinho = relationship("Carrinho", back_populates="itens")
    
    @property
    def subtotal(self):
        return self.preco_unitario * self.quantidade