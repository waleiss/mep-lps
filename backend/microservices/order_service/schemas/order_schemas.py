# Order Schemas - Pydantic models for request/response validation
# Defines data structures for API endpoints

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class OrderItemCreate(BaseModel):
    """Schema for creating an order item"""
    livro_id: int = Field(..., description="ID do livro")
    quantidade: int = Field(..., ge=1, description="Quantidade")
    preco_unitario: float = Field(..., ge=0, description="Preço unitário")
    
    @validator('quantidade')
    def validate_quantidade(cls, v):
        if v < 1:
            raise ValueError('Quantidade deve ser maior que 0')
        return v


class OrderCreate(BaseModel):
    """Schema for creating a new order"""
    usuario_id: int = Field(..., description="ID do usuário")
    endereco_entrega_id: int = Field(..., description="ID do endereço de entrega")
    valor_frete: float = Field(..., ge=0, description="Valor do frete")
    observacoes: Optional[str] = Field(None, max_length=500, description="Observações")
    items: List[OrderItemCreate] = Field(..., min_items=1, description="Itens do pedido")
    
    @validator('items')
    def validate_items(cls, v):
        if not v:
            raise ValueError('Pedido deve ter pelo menos um item')
        return v


class OrderItemResponse(BaseModel):
    """Schema for order item response"""
    id: int
    pedido_id: int
    livro_id: int
    quantidade: int
    preco_unitario: float
    subtotal: float
    data_criacao: Optional[str]
    
    # Book details (from catalog service)
    livro_titulo: Optional[str] = None
    livro_autor: Optional[str] = None
    livro_isbn: Optional[str] = None
    
    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """Schema for order response"""
    id: int
    usuario_id: int
    endereco_entrega_id: int
    numero_pedido: str
    status: str
    valor_total: float
    valor_frete: float
    observacoes: Optional[str]
    data_criacao: Optional[str]
    data_atualizacao: Optional[str]
    data_entrega_prevista: Optional[str]
    data_entrega_realizada: Optional[str]
    items: List[OrderItemResponse]
    
    # Additional details
    usuario_info: Optional[dict] = None
    endereco_entrega: Optional[dict] = None
    pagamento_info: Optional[dict] = None
    
    class Config:
        from_attributes = True


class OrderListResponse(BaseModel):
    """Schema for paginated order list response"""
    items: List[OrderResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool


class OrderStatusUpdate(BaseModel):
    """Schema for updating order status"""
    status: str = Field(..., description="Novo status do pedido")
    
    @validator('status')
    def validate_status(cls, v):
        valid_statuses = ['pendente', 'confirmado', 'processando', 'enviado', 'entregue', 'cancelado', 'devolvido']
        if v not in valid_statuses:
            raise ValueError(f'Status deve ser um dos seguintes: {", ".join(valid_statuses)}')
        return v


class OrderCreateFromCart(BaseModel):
    """Schema for creating order from cart"""
    usuario_id: int = Field(..., description="ID do usuário")
    endereco_entrega_id: int = Field(..., description="ID do endereço de entrega")
    pagamento_id: int = Field(..., description="ID do pagamento")
    observacoes: Optional[str] = Field(None, max_length=500, description="Observações")
