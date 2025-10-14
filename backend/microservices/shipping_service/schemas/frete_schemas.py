# Schemas para cálculo de frete
# Define estruturas para cálculo e cotação de frete

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from decimal import Decimal
import re


class FreteCalculoRequest(BaseModel):
    """Schema para requisição de cálculo de frete"""
    cep_destino: str = Field(..., min_length=8, max_length=9, description="CEP de destino")
    peso_total: Decimal = Field(..., gt=0, description="Peso total em kg")
    valor_produtos: Decimal = Field(..., gt=0, description="Valor total dos produtos")
    
    @validator('cep_destino')
    def validate_cep(cls, v):
        """Valida formato do CEP"""
        cep_limpo = re.sub(r'\D', '', v)
        if len(cep_limpo) != 8:
            raise ValueError('CEP deve conter 8 dígitos')
        return cep_limpo
    
    @validator('peso_total')
    def validate_peso(cls, v):
        """Valida peso"""
        if v <= 0:
            raise ValueError('Peso deve ser maior que zero')
        if v > 30:
            raise ValueError('Peso máximo por envio é 30kg. Para cargas maiores, contacte o suporte.')
        return v


class FreteOpcao(BaseModel):
    """Schema para uma opção de frete"""
    tipo: str = Field(..., description="Tipo de frete (ECONOMICO ou GRATIS)")
    nome: str = Field(..., description="Nome descritivo do frete")
    valor: Decimal = Field(..., ge=0, description="Valor do frete")
    prazo_dias: int = Field(..., gt=0, description="Prazo de entrega em dias")
    descricao: str = Field(..., description="Descrição detalhada")
    
    class Config:
        from_attributes = True


class FreteCalculoResponse(BaseModel):
    """Schema para resposta de cálculo de frete"""
    cep_destino: str
    peso_total: Decimal
    valor_produtos: Decimal
    opcoes_frete: List[FreteOpcao]
    mensagem: Optional[str] = None
    
    class Config:
        from_attributes = True


class ViaCEPResponse(BaseModel):
    """Schema para resposta da API ViaCEP"""
    cep: str
    logradouro: str
    complemento: Optional[str] = ""
    bairro: str
    localidade: str  # cidade
    uf: str  # estado
    ibge: Optional[str] = None
    gia: Optional[str] = None
    ddd: Optional[str] = None
    siafi: Optional[str] = None
    erro: Optional[bool] = False
    
    class Config:
        from_attributes = True

