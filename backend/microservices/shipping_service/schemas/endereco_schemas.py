# Schemas para validação de endereços
# Define estruturas de entrada e saída da API

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
import re


class EnderecoBase(BaseModel):
    """Base schema para endereço"""
    cep: str = Field(..., min_length=8, max_length=9, description="CEP (formato: 12345678 ou 12345-678)")
    logradouro: str = Field(..., min_length=3, max_length=200, description="Rua, avenida, etc")
    numero: str = Field(..., max_length=20, description="Número do imóvel")
    complemento: Optional[str] = Field(None, max_length=100, description="Complemento (apto, bloco, etc)")
    bairro: str = Field(..., min_length=2, max_length=100, description="Bairro")
    cidade: str = Field(..., min_length=2, max_length=100, description="Cidade")
    estado: str = Field(..., min_length=2, max_length=2, description="UF (2 letras)")
    
    @validator('cep')
    def validate_cep(cls, v):
        """Valida formato do CEP"""
        # Remove caracteres não numéricos
        cep_limpo = re.sub(r'\D', '', v)
        if len(cep_limpo) != 8:
            raise ValueError('CEP deve conter 8 dígitos')
        return cep_limpo
    
    @validator('estado')
    def validate_estado(cls, v):
        """Valida UF"""
        estados_validos = [
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
            'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
            'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
        ]
        if v.upper() not in estados_validos:
            raise ValueError(f'Estado inválido. Use uma das UFs: {", ".join(estados_validos)}')
        return v.upper()


class EnderecoCreate(EnderecoBase):
    """Schema para criação de endereço"""
    usuario_id: int = Field(..., gt=0, description="ID do usuário")
    apelido: Optional[str] = Field(None, max_length=50, description="Apelido do endereço (Casa, Trabalho, etc)")
    principal: bool = Field(default=False, description="Define se é o endereço principal")


class EnderecoUpdate(BaseModel):
    """Schema para atualização de endereço"""
    cep: Optional[str] = Field(None, min_length=8, max_length=9)
    logradouro: Optional[str] = Field(None, min_length=3, max_length=200)
    numero: Optional[str] = Field(None, max_length=20)
    complemento: Optional[str] = Field(None, max_length=100)
    bairro: Optional[str] = Field(None, min_length=2, max_length=100)
    cidade: Optional[str] = Field(None, min_length=2, max_length=100)
    estado: Optional[str] = Field(None, min_length=2, max_length=2)
    pais: Optional[str] = Field(None, max_length=50)
    apelido: Optional[str] = Field(None, max_length=50)
    principal: Optional[bool] = None
    ativo: Optional[bool] = None
    
    @validator('cep')
    def validate_cep(cls, v):
        if v is not None:
            cep_limpo = re.sub(r'\D', '', v)
            if len(cep_limpo) != 8:
                raise ValueError('CEP deve conter 8 dígitos')
            return cep_limpo
        return v
    
    @validator('estado')
    def validate_estado(cls, v):
        if v is not None:
            estados_validos = [
                'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
                'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
                'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
            ]
            if v.upper() not in estados_validos:
                raise ValueError(f'Estado inválido. Use uma das UFs: {", ".join(estados_validos)}')
            return v.upper()
        return v


class EnderecoResponse(EnderecoBase):
    """Schema para resposta de endereço"""
    id: int
    usuario_id: int
    apelido: Optional[str]
    principal: bool
    ativo: bool
    data_criacao: datetime
    data_atualizacao: datetime
    
    class Config:
        from_attributes = True


class EnderecoListResponse(BaseModel):
    """Schema para lista de endereços"""
    enderecos: List[EnderecoResponse]
    total: int
    
    class Config:
        from_attributes = True

