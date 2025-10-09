# Modelos de dados para o microserviço de Autenticação
# Define as entidades Usuario, Endereco e enums relacionados
# Implementa o modelo de domínio conforme diagrama UML

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

Base = declarative_base()

class TipoUsuario(enum.Enum):
    CLIENTE = "cliente"
    ADMIN = "admin"
    VENDEDOR = "vendedor"

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    telefone = Column(String(20))
    data_nascimento = Column(DateTime)
    tipo = Column(SQLEnum(TipoUsuario), default=TipoUsuario.CLIENTE)
    ativo = Column(Boolean, default=True)
    data_criacao = Column(DateTime, default=func.now())
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relacionamentos (apenas dentro do mesmo microserviço)
    enderecos = relationship("Endereco", back_populates="usuario", cascade="all, delete-orphan")

class Endereco(Base):
    __tablename__ = "enderecos"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    logradouro = Column(String(255), nullable=False)
    numero = Column(String(10), nullable=False)
    complemento = Column(String(100))
    bairro = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)
    cep = Column(String(9), nullable=False)
    principal = Column(Boolean, default=False)
    data_criacao = Column(DateTime, default=func.now())
    data_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relacionamentos (apenas dentro do mesmo microserviço)
    usuario = relationship("Usuario", back_populates="enderecos")