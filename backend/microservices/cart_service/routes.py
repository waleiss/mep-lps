# Cart Routes - API endpoints for cart operations
# Implements /carrinho, /carrinho/add, /carrinho/remove, /carrinho/update endpoints

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from decimal import Decimal

from database import get_db
from services.cart_service import CartService
from schemas.cart_schemas import (
    AddToCartRequest,
    UpdateCartItemRequest,
    RemoveFromCartRequest,
    CartResponse,
    CartDetailResponse,
    CartActionResponse,
    CartSummary
)
from models import Carrinho

# Create router
router = APIRouter()


# Helper function to convert cart to response
def cart_to_response(cart: Carrinho) -> CartResponse:
    """Convert cart model to response schema"""
    return CartResponse(
        id=cart.id,
        usuario_id=cart.usuario_id,
        ativo=cart.ativo,
        itens=[
            {
                "id": item.id,
                "livro_id": item.livro_id,
                "quantidade": item.quantidade,
                "preco_unitario": item.preco_unitario,
                "subtotal": item.subtotal,
                "data_criacao": item.data_criacao,
                "data_atualizacao": item.data_atualizacao
            }
            for item in cart.itens
        ],
        total_itens=cart.total_itens,
        valor_total=cart.valor_total,
        data_criacao=cart.data_criacao,
        data_atualizacao=cart.data_atualizacao
    )


# Health endpoints
@router.get("/")
async def root():
    """Endpoint raiz do serviço de carrinho"""
    return {
        "service": "Cart Service",
        "status": "running",
        "version": "1.0.0"
    }


@router.get("/health")
async def health_check():
    """Health check do serviço"""
    return {"status": "healthy", "service": "cart"}


# Cart endpoints
@router.get("/carrinho/{usuario_id}", response_model=CartDetailResponse)
async def get_cart(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    """
    Obter carrinho do usuário
    
    Args:
        usuario_id: ID do usuário
        
    Returns:
        Dados completos do carrinho
    """
    cart_service = CartService(db)
    
    try:
        cart = cart_service.get_cart(usuario_id)
        cart_response = cart_to_response(cart)
        summary = CartSummary(
            total_itens=cart.total_itens,
            subtotal=cart.valor_total,
            valor_total=cart.valor_total
        )
        
        return CartDetailResponse(
            carrinho=cart_response,
            resumo=summary
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao obter carrinho: {str(e)}"
        )


@router.post("/carrinho/{usuario_id}/add", response_model=CartActionResponse)
async def add_to_cart(
    usuario_id: int,
    request: AddToCartRequest,
    db: Session = Depends(get_db)
):
    """
    Adicionar item ao carrinho
    
    Args:
        usuario_id: ID do usuário
        request: Dados do item a adicionar
        
    Returns:
        Carrinho atualizado com mensagem de sucesso
    """
    cart_service = CartService(db)
    
    try:
        # TODO: Em produção, buscar preço do catalog_service
        # Por enquanto, usar preço mock
        preco_unitario = Decimal("29.90")
        
        cart = cart_service.add_item_to_cart(
            usuario_id=usuario_id,
            livro_id=request.livro_id,
            quantidade=request.quantidade,
            preco_unitario=preco_unitario
        )
        
        cart_response = cart_to_response(cart)
        summary = CartSummary(
            total_itens=cart.total_itens,
            subtotal=cart.valor_total,
            valor_total=cart.valor_total
        )
        
        return CartActionResponse(
            message="Item adicionado ao carrinho com sucesso",
            carrinho=cart_response,
            resumo=summary
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao adicionar item ao carrinho: {str(e)}"
        )


@router.put("/carrinho/{usuario_id}/update/{livro_id}", response_model=CartActionResponse)
async def update_cart_item(
    usuario_id: int,
    livro_id: int,
    request: UpdateCartItemRequest,
    db: Session = Depends(get_db)
):
    """
    Atualizar quantidade de item no carrinho
    
    Args:
        usuario_id: ID do usuário
        livro_id: ID do livro
        request: Nova quantidade
        
    Returns:
        Carrinho atualizado com mensagem de sucesso
    """
    cart_service = CartService(db)
    
    try:
        cart = cart_service.update_item_quantity(
            usuario_id=usuario_id,
            livro_id=livro_id,
            quantidade=request.quantidade
        )
        
        cart_response = cart_to_response(cart)
        summary = CartSummary(
            total_itens=cart.total_itens,
            subtotal=cart.valor_total,
            valor_total=cart.valor_total
        )
        
        message = "Item removido do carrinho" if request.quantidade == 0 else "Quantidade atualizada com sucesso"
        
        return CartActionResponse(
            message=message,
            carrinho=cart_response,
            resumo=summary
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar item: {str(e)}"
        )


@router.delete("/carrinho/{usuario_id}/remove/{livro_id}", response_model=CartActionResponse)
async def remove_from_cart(
    usuario_id: int,
    livro_id: int,
    db: Session = Depends(get_db)
):
    """
    Remover item do carrinho
    
    Args:
        usuario_id: ID do usuário
        livro_id: ID do livro a remover
        
    Returns:
        Carrinho atualizado com mensagem de sucesso
    """
    cart_service = CartService(db)
    
    try:
        cart = cart_service.remove_item_from_cart(
            usuario_id=usuario_id,
            livro_id=livro_id
        )
        
        cart_response = cart_to_response(cart)
        summary = CartSummary(
            total_itens=cart.total_itens,
            subtotal=cart.valor_total,
            valor_total=cart.valor_total
        )
        
        return CartActionResponse(
            message="Item removido do carrinho com sucesso",
            carrinho=cart_response,
            resumo=summary
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover item: {str(e)}"
        )


@router.delete("/carrinho/{usuario_id}/clear", response_model=CartActionResponse)
async def clear_cart(
    usuario_id: int,
    db: Session = Depends(get_db)
):
    """
    Limpar todos os itens do carrinho
    
    Args:
        usuario_id: ID do usuário
        
    Returns:
        Carrinho vazio com mensagem de sucesso
    """
    cart_service = CartService(db)
    
    try:
        cart = cart_service.clear_cart(usuario_id)
        
        cart_response = cart_to_response(cart)
        summary = CartSummary(
            total_itens=0,
            subtotal=Decimal("0.00"),
            valor_total=Decimal("0.00")
        )
        
        return CartActionResponse(
            message="Carrinho limpo com sucesso",
            carrinho=cart_response,
            resumo=summary
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao limpar carrinho: {str(e)}"
        )