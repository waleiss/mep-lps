# Schemas para validação de pagamentos
# Define estruturas de entrada e saída da API

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
import re


class PagamentoCartaoRequest(BaseModel):
    """Schema para pagamento com cartão de crédito/débito"""
    usuario_id: int = Field(..., gt=0, description="ID do usuário")
    pedido_id: int = Field(..., gt=0, description="ID do pedido")
    valor: Decimal = Field(..., gt=0, description="Valor do pagamento")
    numero_cartao: str = Field(..., min_length=13, max_length=19, description="Número do cartão")
    nome_titular: str = Field(..., min_length=3, max_length=100, description="Nome do titular")
    validade: str = Field(..., pattern=r"^\d{2}/\d{2}$", description="Validade MM/YY")
    cvv: str = Field(..., min_length=3, max_length=4, description="Código de segurança")
    parcelas: int = Field(default=1, ge=1, le=12, description="Número de parcelas")
    
    @validator('numero_cartao')
    def validate_card_number(cls, v):
        """Remove espaços e valida tamanho"""
        card = v.replace(' ', '').replace('-', '')
        if not card.isdigit():
            raise ValueError('Número do cartão deve conter apenas dígitos')
        if len(card) < 13 or len(card) > 19:
            raise ValueError('Número do cartão inválido')
        return card
    
    @validator('cvv')
    def validate_cvv(cls, v):
        """Valida CVV"""
        if not v.isdigit():
            raise ValueError('CVV deve conter apenas dígitos')
        return v


class PagamentoPixRequest(BaseModel):
    """Schema para pagamento via PIX"""
    usuario_id: int = Field(..., gt=0, description="ID do usuário")
    pedido_id: int = Field(..., gt=0, description="ID do pedido")
    valor: Decimal = Field(..., gt=0, description="Valor do pagamento")


class PagamentoBoletoRequest(BaseModel):
    """Schema para pagamento via Boleto"""
    usuario_id: int = Field(..., gt=0, description="ID do usuário")
    pedido_id: int = Field(..., gt=0, description="ID do pedido")
    valor: Decimal = Field(..., gt=0, description="Valor do pagamento")
    cpf_cnpj: str = Field(..., description="CPF ou CNPJ do pagador")
    
    @validator('cpf_cnpj')
    def validate_cpf_cnpj(cls, v):
        """Valida CPF ou CNPJ com dígitos verificadores"""
        from utils.validators import validar_cpf_cnpj
        
        doc_limpo = re.sub(r'\D', '', v)
        valido, tipo = validar_cpf_cnpj(doc_limpo)
        
        if not valido:
            raise ValueError(f'CPF/CNPJ inválido. Verifique os dígitos verificadores.')
        
        return doc_limpo


class PagamentoCreate(BaseModel):
    """Schema genérico para criação de pagamento"""
    usuario_id: int
    pedido_id: int
    forma_pagamento: str
    valor: Decimal
    dados_pagamento: Optional[dict] = None


class PagamentoResponse(BaseModel):
    """Schema para resposta de pagamento"""
    id: int
    usuario_id: int
    pedido_id: int
    forma_pagamento: str
    status: str
    valor: Decimal
    codigo_transacao: str
    dados_pagamento: Optional[str] = None
    data_processamento: Optional[datetime] = None
    data_aprovacao: Optional[datetime] = None
    observacoes: Optional[str] = None
    data_criacao: datetime
    data_atualizacao: datetime
    
    # Campos extras para respostas específicas
    mensagem: Optional[str] = None
    qr_code: Optional[str] = None  # Para PIX
    codigo_barras: Optional[str] = None  # Para Boleto
    linha_digitavel: Optional[str] = None  # Para Boleto
    
    class Config:
        from_attributes = True


class StatusPagamentoResponse(BaseModel):
    """Schema para consulta de status de pagamento"""
    id: int
    pedido_id: int
    status: str
    forma_pagamento: str
    valor: Decimal
    codigo_transacao: str
    data_criacao: datetime
    data_processamento: Optional[datetime]
    data_aprovacao: Optional[datetime]
    mensagem: str
    
    class Config:
        from_attributes = True


class TransacaoLogResponse(BaseModel):
    """Schema para log de transação"""
    id: int
    usuario_id: int
    pedido_id: int
    forma_pagamento: str
    status: str
    valor: Decimal
    codigo_transacao: str
    data_criacao: datetime
    
    class Config:
        from_attributes = True


class PagamentoListResponse(BaseModel):
    """Schema para lista de pagamentos"""
    pagamentos: List[TransacaoLogResponse]
    total: int
    
    class Config:
        from_attributes = True

