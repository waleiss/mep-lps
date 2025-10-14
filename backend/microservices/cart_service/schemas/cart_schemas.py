# Cart Schemas - Pydantic models for request/response validation
# Defines data models for cart endpoints

from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field, validator


class CartItemBase(BaseModel):
    """Base schema for cart item"""
    livro_id: int = Field(..., description="ID do livro no catálogo")
    quantidade: int = Field(1, ge=1, le=99, description="Quantidade do item")
    preco_unitario: Decimal = Field(..., ge=0, description="Preço unitário do livro")


class AddToCartRequest(BaseModel):
    """Request schema for adding item to cart"""
    livro_id: int = Field(..., description="ID do livro a ser adicionado")
    quantidade: int = Field(1, ge=1, le=99, description="Quantidade a adicionar")
    
    @validator('quantidade')
    def validate_quantidade(cls, v):
        if v < 1:
            raise ValueError('Quantidade deve ser pelo menos 1')
        if v > 99:
            raise ValueError('Quantidade não pode exceder 99 unidades')
        return v


class UpdateCartItemRequest(BaseModel):
    """Request schema for updating cart item quantity"""
    quantidade: int = Field(..., ge=0, le=99, description="Nova quantidade (0 para remover)")
    
    @validator('quantidade')
    def validate_quantidade(cls, v):
        if v < 0:
            raise ValueError('Quantidade não pode ser negativa')
        if v > 99:
            raise ValueError('Quantidade não pode exceder 99 unidades')
        return v


class RemoveFromCartRequest(BaseModel):
    """Request schema for removing item from cart"""
    livro_id: int = Field(..., description="ID do livro a ser removido")


class CartItemResponse(BaseModel):
    """Response schema for cart item"""
    id: int
    livro_id: int
    quantidade: int
    preco_unitario: Decimal
    subtotal: Decimal
    data_criacao: datetime
    data_atualizacao: datetime
    
    class Config:
        from_attributes = True


class CartSummary(BaseModel):
    """Summary of cart totals"""
    total_itens: int = Field(..., description="Total de itens no carrinho")
    subtotal: Decimal = Field(..., description="Subtotal dos itens")
    valor_total: Decimal = Field(..., description="Valor total do carrinho")


class CartResponse(BaseModel):
    """Response schema for cart data"""
    id: int
    usuario_id: int
    ativo: bool
    itens: List[CartItemResponse]
    total_itens: int
    valor_total: Decimal
    data_criacao: datetime
    data_atualizacao: datetime
    
    class Config:
        from_attributes = True


class CartDetailResponse(BaseModel):
    """Detailed cart response with summary"""
    carrinho: CartResponse
    resumo: CartSummary


class CartActionResponse(BaseModel):
    """Response schema for cart actions (add, update, remove)"""
    message: str
    carrinho: CartResponse
    resumo: CartSummary
