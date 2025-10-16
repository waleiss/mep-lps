# Order Repository - Data access layer for order operations
# Implements repository pattern for order data access

from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, asc
from datetime import datetime

from models import Pedido, ItemPedido, StatusPedido


class OrderRepository:
    """Repository for order data operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_order(self, order_data: dict, items_data: List[dict]) -> Pedido:
        """
        Create a new order with items
        
        Args:
            order_data: Order data dictionary
            items_data: List of order items data
            
        Returns:
            Created order instance
        """
        # Create order
        db_order = Pedido(**order_data)
        self.db.add(db_order)
        self.db.flush()  # Get order ID without committing
        
        # Create order items
        for item_data in items_data:
            item_data['pedido_id'] = db_order.id
            db_item = ItemPedido(**item_data)
            self.db.add(db_item)
        
        self.db.commit()
        self.db.refresh(db_order)
        return db_order
    
    def get_by_id(self, order_id: int) -> Optional[Pedido]:
        """
        Get order by ID with items
        
        Args:
            order_id: Order ID
            
        Returns:
            Order instance or None if not found
        """
        return self.db.query(Pedido).filter(Pedido.id == order_id).first()
    
    def get_by_numero_pedido(self, numero_pedido: str) -> Optional[Pedido]:
        """
        Get order by order number
        
        Args:
            numero_pedido: Order number
            
        Returns:
            Order instance or None if not found
        """
        return self.db.query(Pedido).filter(
            Pedido.numero_pedido == numero_pedido
        ).first()
    
    def get_by_usuario(
        self,
        usuario_id: int,
        skip: int = 0,
        limit: int = 20,
        status: Optional[StatusPedido] = None,
        order_by: str = "data_criacao",
        order_direction: str = "desc"
    ) -> Tuple[List[Pedido], int]:
        """
        Get orders by user with filters and pagination
        
        Args:
            usuario_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return
            status: Filter by status
            order_by: Field to order by
            order_direction: Order direction (asc or desc)
            
        Returns:
            Tuple of (list of orders, total count)
        """
        query = self.db.query(Pedido).filter(Pedido.usuario_id == usuario_id)
        
        # Apply status filter
        if status:
            query = query.filter(Pedido.status == status)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply ordering
        order_field = getattr(Pedido, order_by, Pedido.data_criacao)
        if order_direction == "asc":
            query = query.order_by(asc(order_field))
        else:
            query = query.order_by(desc(order_field))
        
        # Apply pagination
        orders = query.offset(skip).limit(limit).all()
        
        return orders, total
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 20,
        status: Optional[StatusPedido] = None,
        order_by: str = "data_criacao",
        order_direction: str = "desc"
    ) -> Tuple[List[Pedido], int]:
        """
        Get all orders with filters and pagination (Admin)
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            status: Filter by status
            order_by: Field to order by
            order_direction: Order direction (asc or desc)
            
        Returns:
            Tuple of (list of orders, total count)
        """
        query = self.db.query(Pedido)
        
        # Apply status filter
        if status:
            query = query.filter(Pedido.status == status)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply ordering
        order_field = getattr(Pedido, order_by, Pedido.data_criacao)
        if order_direction == "asc":
            query = query.order_by(asc(order_field))
        else:
            query = query.order_by(desc(order_field))
        
        # Apply pagination
        orders = query.offset(skip).limit(limit).all()
        
        return orders, total
    
    def update_status(self, order_id: int, status: StatusPedido) -> Optional[Pedido]:
        """
        Update order status
        
        Args:
            order_id: Order ID
            status: New status
            
        Returns:
            Updated order instance or None if not found
        """
        order = self.get_by_id(order_id)
        if not order:
            return None
        
        order.status = status
        
        # Update delivery date if status is ENTREGUE
        if status == StatusPedido.ENTREGUE:
            order.data_entrega_realizada = datetime.now()
        
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def update(self, order_id: int, update_data: dict) -> Optional[Pedido]:
        """
        Update order data
        
        Args:
            order_id: Order ID
            update_data: Dictionary with fields to update
            
        Returns:
            Updated order instance or None if not found
        """
        order = self.get_by_id(order_id)
        if not order:
            return None
        
        for field, value in update_data.items():
            if hasattr(order, field):
                setattr(order, field, value)
        
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def numero_pedido_exists(self, numero_pedido: str) -> bool:
        """
        Check if order number already exists
        
        Args:
            numero_pedido: Order number to check
            
        Returns:
            True if exists, False otherwise
        """
        return self.db.query(Pedido).filter(
            Pedido.numero_pedido == numero_pedido
        ).first() is not None
    
    def get_last_order_number(self) -> Optional[str]:
        """
        Get the last order number created
        
        Returns:
            Last order number or None
        """
        order = self.db.query(Pedido).order_by(desc(Pedido.id)).first()
        return order.numero_pedido if order else None
