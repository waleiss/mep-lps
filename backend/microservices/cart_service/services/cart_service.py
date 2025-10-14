# Cart Service - Business logic for cart operations
# Handles cart management, item operations, and cache synchronization

from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from decimal import Decimal

from models import Carrinho, ItemCarrinho
from repositories.cart_repository import CartRepository
from services.redis_service import redis_service
from config import settings


class CartService:
    """Service for cart business logic operations"""
    
    def __init__(self, db: Session):
        self.cart_repo = CartRepository(db)
        self.redis_service = redis_service
    
    def _serialize_cart(self, cart: Carrinho) -> Dict[str, Any]:
        """
        Serialize cart object to dictionary
        
        Args:
            cart: Cart instance
            
        Returns:
            Cart data dictionary
        """
        return {
            "id": cart.id,
            "usuario_id": cart.usuario_id,
            "ativo": cart.ativo,
            "itens": [
                {
                    "id": item.id,
                    "livro_id": item.livro_id,
                    "quantidade": item.quantidade,
                    "preco_unitario": float(item.preco_unitario),
                    "subtotal": float(item.subtotal),
                    "data_criacao": item.data_criacao.isoformat(),
                    "data_atualizacao": item.data_atualizacao.isoformat()
                }
                for item in cart.itens
            ],
            "total_itens": cart.total_itens,
            "valor_total": float(cart.valor_total),
            "data_criacao": cart.data_criacao.isoformat(),
            "data_atualizacao": cart.data_atualizacao.isoformat()
        }
    
    def _sync_to_cache(self, cart: Carrinho) -> None:
        """
        Synchronize cart to Redis cache
        
        Args:
            cart: Cart instance
        """
        if self.redis_service.is_connected():
            cart_data = self._serialize_cart(cart)
            self.redis_service.set_cart(cart.usuario_id, cart_data)
    
    def get_cart(self, usuario_id: int) -> Carrinho:
        """
        Get cart for user
        
        Args:
            usuario_id: User ID
            
        Returns:
            Cart instance
        """
        # Try to get from cache first
        cached_cart = self.redis_service.get_cart(usuario_id)
        if cached_cart:
            # Refresh TTL
            self.redis_service.refresh_ttl(usuario_id)
        
        # Get or create cart from database
        cart = self.cart_repo.get_or_create_cart(usuario_id)
        
        # Sync to cache
        self._sync_to_cache(cart)
        
        return cart
    
    def add_item_to_cart(
        self, 
        usuario_id: int, 
        livro_id: int, 
        quantidade: int,
        preco_unitario: Decimal
    ) -> Carrinho:
        """
        Add item to cart or update quantity if exists
        
        Args:
            usuario_id: User ID
            livro_id: Book ID
            quantidade: Quantity to add
            preco_unitario: Unit price
            
        Returns:
            Updated cart instance
            
        Raises:
            HTTPException: If validation fails
        """
        # Validate quantity
        if quantidade < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantidade deve ser pelo menos 1"
            )
        
        if quantidade > settings.max_quantity_per_item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Quantidade não pode exceder {settings.max_quantity_per_item} unidades"
            )
        
        # Validate price
        if preco_unitario <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Preço deve ser maior que zero"
            )
        
        # Get or create cart
        cart = self.cart_repo.get_or_create_cart(usuario_id)
        
        # Check if item already exists
        existing_item = self.cart_repo.get_item_by_book(cart.id, livro_id)
        
        if existing_item:
            # Update quantity
            new_quantity = existing_item.quantidade + quantidade
            
            if new_quantity > settings.max_quantity_per_item:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Quantidade total não pode exceder {settings.max_quantity_per_item} unidades"
                )
            
            self.cart_repo.update_item_quantity(existing_item.id, new_quantity)
        else:
            # Add new item
            self.cart_repo.add_item(cart.id, livro_id, quantidade, preco_unitario)
        
        # Refresh cart
        cart = self.cart_repo.get_cart_by_id(cart.id)
        
        # Sync to cache
        self._sync_to_cache(cart)
        
        return cart
    
    def update_item_quantity(
        self, 
        usuario_id: int, 
        livro_id: int, 
        quantidade: int
    ) -> Carrinho:
        """
        Update item quantity in cart
        
        Args:
            usuario_id: User ID
            livro_id: Book ID
            quantidade: New quantity (0 to remove)
            
        Returns:
            Updated cart instance
            
        Raises:
            HTTPException: If validation fails or item not found
        """
        # Validate quantity
        if quantidade < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantidade não pode ser negativa"
            )
        
        if quantidade > settings.max_quantity_per_item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Quantidade não pode exceder {settings.max_quantity_per_item} unidades"
            )
        
        # Get cart
        cart = self.cart_repo.get_active_cart_by_user(usuario_id)
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carrinho não encontrado"
            )
        
        # Get item
        item = self.cart_repo.get_item_by_book(cart.id, livro_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item não encontrado no carrinho"
            )
        
        # Update or remove
        if quantidade == 0:
            self.cart_repo.delete_item(item.id)
        else:
            self.cart_repo.update_item_quantity(item.id, quantidade)
        
        # Refresh cart
        cart = self.cart_repo.get_cart_by_id(cart.id)
        
        # Sync to cache
        self._sync_to_cache(cart)
        
        return cart
    
    def remove_item_from_cart(self, usuario_id: int, livro_id: int) -> Carrinho:
        """
        Remove item from cart
        
        Args:
            usuario_id: User ID
            livro_id: Book ID
            
        Returns:
            Updated cart instance
            
        Raises:
            HTTPException: If cart or item not found
        """
        # Get cart
        cart = self.cart_repo.get_active_cart_by_user(usuario_id)
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carrinho não encontrado"
            )
        
        # Remove item
        success = self.cart_repo.delete_item_by_book(cart.id, livro_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item não encontrado no carrinho"
            )
        
        # Refresh cart
        cart = self.cart_repo.get_cart_by_id(cart.id)
        
        # Sync to cache
        self._sync_to_cache(cart)
        
        return cart
    
    def clear_cart(self, usuario_id: int) -> Carrinho:
        """
        Clear all items from cart
        
        Args:
            usuario_id: User ID
            
        Returns:
            Empty cart instance
            
        Raises:
            HTTPException: If cart not found
        """
        # Get cart
        cart = self.cart_repo.get_active_cart_by_user(usuario_id)
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Carrinho não encontrado"
            )
        
        # Clear items
        self.cart_repo.clear_cart(cart.id)
        
        # Refresh cart
        cart = self.cart_repo.get_cart_by_id(cart.id)
        
        # Sync to cache
        self._sync_to_cache(cart)
        
        return cart
    
    def get_cart_summary(self, cart: Carrinho) -> Dict[str, Any]:
        """
        Get cart summary with totals
        
        Args:
            cart: Cart instance
            
        Returns:
            Cart summary dictionary
        """
        return {
            "total_itens": cart.total_itens,
            "subtotal": cart.valor_total,
            "valor_total": cart.valor_total
        }
