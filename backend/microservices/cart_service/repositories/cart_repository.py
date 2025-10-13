# Cart Repository - Data access layer for cart operations
# Implements repository pattern for cart data access

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_
from decimal import Decimal

from models import Carrinho, ItemCarrinho


class CartRepository:
    """Repository for cart data operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ========== Cart Operations ==========
    
    def create_cart(self, usuario_id: int) -> Carrinho:
        """
        Create a new cart for a user
        
        Args:
            usuario_id: User ID
            
        Returns:
            Created cart instance
        """
        db_cart = Carrinho(usuario_id=usuario_id, ativo=True)
        self.db.add(db_cart)
        self.db.commit()
        self.db.refresh(db_cart)
        return db_cart
    
    def get_cart_by_id(self, cart_id: int) -> Optional[Carrinho]:
        """
        Get cart by ID
        
        Args:
            cart_id: Cart ID
            
        Returns:
            Cart instance or None if not found
        """
        return self.db.query(Carrinho).filter(Carrinho.id == cart_id).first()
    
    def get_active_cart_by_user(self, usuario_id: int) -> Optional[Carrinho]:
        """
        Get active cart for a user
        
        Args:
            usuario_id: User ID
            
        Returns:
            Active cart instance or None if not found
        """
        return self.db.query(Carrinho).filter(
            and_(Carrinho.usuario_id == usuario_id, Carrinho.ativo == True)
        ).first()
    
    def get_or_create_cart(self, usuario_id: int) -> Carrinho:
        """
        Get active cart for user or create if doesn't exist
        
        Args:
            usuario_id: User ID
            
        Returns:
            Cart instance
        """
        cart = self.get_active_cart_by_user(usuario_id)
        if not cart:
            cart = self.create_cart(usuario_id)
        return cart
    
    def deactivate_cart(self, cart_id: int) -> bool:
        """
        Deactivate a cart (set ativo = False)
        
        Args:
            cart_id: Cart ID
            
        Returns:
            True if successful, False otherwise
        """
        cart = self.get_cart_by_id(cart_id)
        if not cart:
            return False
        
        cart.ativo = False
        self.db.commit()
        return True
    
    def clear_cart(self, cart_id: int) -> bool:
        """
        Remove all items from cart
        
        Args:
            cart_id: Cart ID
            
        Returns:
            True if successful, False otherwise
        """
        cart = self.get_cart_by_id(cart_id)
        if not cart:
            return False
        
        # Delete all items
        self.db.query(ItemCarrinho).filter(
            ItemCarrinho.carrinho_id == cart_id
        ).delete()
        
        self.db.commit()
        return True
    
    # ========== Cart Item Operations ==========
    
    def add_item(self, carrinho_id: int, livro_id: int, quantidade: int, preco_unitario: Decimal) -> ItemCarrinho:
        """
        Add item to cart
        
        Args:
            carrinho_id: Cart ID
            livro_id: Book ID
            quantidade: Quantity
            preco_unitario: Unit price
            
        Returns:
            Created cart item instance
        """
        db_item = ItemCarrinho(
            carrinho_id=carrinho_id,
            livro_id=livro_id,
            quantidade=quantidade,
            preco_unitario=preco_unitario
        )
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item
    
    def get_item_by_id(self, item_id: int) -> Optional[ItemCarrinho]:
        """
        Get cart item by ID
        
        Args:
            item_id: Item ID
            
        Returns:
            Cart item instance or None if not found
        """
        return self.db.query(ItemCarrinho).filter(ItemCarrinho.id == item_id).first()
    
    def get_item_by_book(self, carrinho_id: int, livro_id: int) -> Optional[ItemCarrinho]:
        """
        Get cart item by cart ID and book ID
        
        Args:
            carrinho_id: Cart ID
            livro_id: Book ID
            
        Returns:
            Cart item instance or None if not found
        """
        return self.db.query(ItemCarrinho).filter(
            and_(
                ItemCarrinho.carrinho_id == carrinho_id,
                ItemCarrinho.livro_id == livro_id
            )
        ).first()
    
    def get_cart_items(self, carrinho_id: int) -> List[ItemCarrinho]:
        """
        Get all items in a cart
        
        Args:
            carrinho_id: Cart ID
            
        Returns:
            List of cart items
        """
        return self.db.query(ItemCarrinho).filter(
            ItemCarrinho.carrinho_id == carrinho_id
        ).all()
    
    def update_item_quantity(self, item_id: int, quantidade: int) -> Optional[ItemCarrinho]:
        """
        Update cart item quantity
        
        Args:
            item_id: Item ID
            quantidade: New quantity
            
        Returns:
            Updated cart item instance or None if not found
        """
        item = self.get_item_by_id(item_id)
        if not item:
            return None
        
        item.quantidade = quantidade
        self.db.commit()
        self.db.refresh(item)
        return item
    
    def delete_item(self, item_id: int) -> bool:
        """
        Delete cart item
        
        Args:
            item_id: Item ID
            
        Returns:
            True if successful, False otherwise
        """
        item = self.get_item_by_id(item_id)
        if not item:
            return False
        
        self.db.delete(item)
        self.db.commit()
        return True
    
    def delete_item_by_book(self, carrinho_id: int, livro_id: int) -> bool:
        """
        Delete cart item by book ID
        
        Args:
            carrinho_id: Cart ID
            livro_id: Book ID
            
        Returns:
            True if successful, False otherwise
        """
        item = self.get_item_by_book(carrinho_id, livro_id)
        if not item:
            return False
        
        self.db.delete(item)
        self.db.commit()
        return True
    
    def get_cart_total_items(self, carrinho_id: int) -> int:
        """
        Get total number of items in cart
        
        Args:
            carrinho_id: Cart ID
            
        Returns:
            Total number of items
        """
        items = self.get_cart_items(carrinho_id)
        return sum(item.quantidade for item in items)
    
    def get_cart_total_value(self, carrinho_id: int) -> Decimal:
        """
        Get total value of cart
        
        Args:
            carrinho_id: Cart ID
            
        Returns:
            Total cart value
        """
        items = self.get_cart_items(carrinho_id)
        return sum(item.preco_unitario * item.quantidade for item in items)
