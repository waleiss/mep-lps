# Rotas da API REST para pedidos
# Endpoints: /pedidos, /pedidos/{id}, /historico
# Implementa RF4.4, RF4.5, RF4.6

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from schemas.order_schemas import (
    OrderCreate,
    OrderResponse,
    OrderListResponse,
    OrderStatusUpdate,
    OrderCreateFromCart
)
from services.order_service import OrderService

router = APIRouter(tags=["Pedidos"])


def get_order_service(db: Session = Depends(get_db)) -> OrderService:
    """Dependency to get order service instance"""
    return OrderService(db)


@router.post("/pedidos", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    order_service: OrderService = Depends(get_order_service)
):
    """
    Criar um novo pedido
    
    Requer dados completos do pedido incluindo itens
    """
    return order_service.create_order(order_data.model_dump())


@router.post("/pedidos/from-cart", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order_from_cart(
    order_data: OrderCreateFromCart,
    order_service: OrderService = Depends(get_order_service)
):
    """
    Criar pedido a partir do carrinho após confirmação de pagamento
    
    - **usuario_id**: ID do usuário
    - **endereco_entrega_id**: ID do endereço de entrega
    - **pagamento_id**: ID do pagamento confirmado
    - **observacoes**: Observações opcionais
    """
    return await order_service.create_order_from_cart(
        usuario_id=order_data.usuario_id,
        endereco_entrega_id=order_data.endereco_entrega_id,
        pagamento_id=order_data.pagamento_id,
        observacoes=order_data.observacoes
    )


@router.get("/pedidos/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    order_service: OrderService = Depends(get_order_service)
):
    """
    Obter detalhes de um pedido específico
    
    - **order_id**: ID do pedido
    """
    return order_service.get_order_by_id(order_id)


@router.get("/pedidos/numero/{numero_pedido}", response_model=OrderResponse)
async def get_order_by_number(
    numero_pedido: str,
    order_service: OrderService = Depends(get_order_service)
):
    """
    Obter detalhes de um pedido pelo número do pedido
    
    - **numero_pedido**: Número do pedido (ex: MP-20241016-0001)
    """
    return order_service.get_order_by_numero(numero_pedido)


@router.get("/historico/{usuario_id}", response_model=OrderListResponse)
async def get_user_order_history(
    usuario_id: int,
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(20, ge=1, le=100, description="Itens por página"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    order_service: OrderService = Depends(get_order_service)
):
    """
    Obter histórico de pedidos do usuário
    
    - **usuario_id**: ID do usuário
    - **page**: Número da página (começa em 1)
    - **page_size**: Quantidade de itens por página (máx: 100)
    - **status**: Filtrar por status (pendente, confirmado, processando, enviado, entregue, cancelado, devolvido)
    """
    return order_service.get_user_orders(
        usuario_id=usuario_id,
        page=page,
        page_size=page_size,
        status=status
    )


@router.get("/pedidos", response_model=OrderListResponse)
async def get_all_orders(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(20, ge=1, le=100, description="Itens por página"),
    status: Optional[str] = Query(None, description="Filtrar por status"),
    usuario_id: Optional[int] = Query(None, description="Filtrar por ID do usuário"),
    order_service: OrderService = Depends(get_order_service)
):
    """
    Listar pedidos
    
    - **page**: Número da página (começa em 1)
    - **page_size**: Quantidade de itens por página (máx: 100)
    - **status**: Filtrar por status
    - **usuario_id**: Filtrar por ID do usuário
    """
    return order_service.get_all_orders(
        page=page,
        page_size=page_size,
        status=status,
        usuario_id=usuario_id
    )


@router.patch("/pedidos/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    order_service: OrderService = Depends(get_order_service)
):
    """
    Atualizar status do pedido (Admin)
    
    - **order_id**: ID do pedido
    - **status**: Novo status (pendente, confirmado, processando, enviado, entregue, cancelado, devolvido)
    """
    return order_service.update_order_status(order_id, status_update.status)