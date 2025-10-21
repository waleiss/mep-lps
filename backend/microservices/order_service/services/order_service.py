# Order Service - Business logic for order operations
# Handles order creation, status updates, and history

from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime, timedelta
import httpx

from models import Pedido, ItemPedido, StatusPedido
from repositories.order_repository import OrderRepository
from services.order_number_service import order_number_service
from config import settings


class OrderService:
    """Service for order business logic operations"""
    
    def __init__(self, db: Session):
        self.order_repo = OrderRepository(db)
        self.order_number_service = order_number_service
    
    def _serialize_item(self, item: ItemPedido, book_details: Optional[dict] = None) -> Dict[str, Any]:
        """
        Serialize order item to dictionary
        
        Args:
            item: ItemPedido instance
            book_details: Optional book details from catalog service
            
        Returns:
            Dictionary representation of order item
        """
        item_dict = {
            "id": item.id,
            "pedido_id": item.pedido_id,
            "livro_id": item.livro_id,
            "quantidade": item.quantidade,
            "preco_unitario": float(item.preco_unitario),
            "subtotal": float(item.preco_unitario * item.quantidade),
            "data_criacao": item.data_criacao.isoformat() if item.data_criacao else None
        }
        
        # Add book details if available
        if book_details:
            item_dict["livro_titulo"] = book_details.get("titulo")
            item_dict["livro_autor"] = book_details.get("autor")
            item_dict["livro_isbn"] = book_details.get("isbn")
        
        return item_dict
    
    def _serialize_order(self, order: Pedido, include_details: bool = False) -> Dict[str, Any]:
        """
        Serialize order to dictionary
        
        Args:
            order: Pedido instance
            include_details: Whether to include external service details
            
        Returns:
            Dictionary representation of order
        """
        order_dict = {
            "id": order.id,
            "usuario_id": order.usuario_id,
            "endereco_entrega_id": order.endereco_entrega_id,
            "numero_pedido": order.numero_pedido,
            "status": order.status.value if order.status else None,
            "valor_total": float(order.valor_total),
            "valor_frete": float(order.valor_frete),
            "observacoes": order.observacoes,
            "data_criacao": order.data_criacao.isoformat() if order.data_criacao else None,
            "data_atualizacao": order.data_atualizacao.isoformat() if order.data_atualizacao else None,
            "data_entrega_prevista": order.data_entrega_prevista.isoformat() if order.data_entrega_prevista else None,
            "data_entrega_realizada": order.data_entrega_realizada.isoformat() if order.data_entrega_realizada else None,
            "items": []
        }
        
        # Serialize items
        for item in order.itens:
            order_dict["items"].append(self._serialize_item(item))
        
        # Add external details if requested
        if include_details:
            # TODO: Fetch address details from shipping service
            # TODO: Fetch payment details from payment service
            pass
        
        return order_dict
    
    async def _fetch_book_details(self, livro_id: int) -> Optional[Dict[str, Any]]:
        """
        Fetch book details from catalog service
        
        Args:
            livro_id: Book ID
            
        Returns:
            Book details dictionary or None
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.catalog_service_url}/livros/{livro_id}",
                    timeout=5.0
                )
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Error fetching book details: {e}")
        return None
    
    async def _fetch_cart_items(self, usuario_id: int) -> List[Dict[str, Any]]:
        """
        Fetch cart items from cart service
        
        Args:
            usuario_id: User ID
            
        Returns:
            List of cart items
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.cart_service_url}/carrinho/{usuario_id}",
                    timeout=5.0
                )
                if response.status_code == 200:
                    cart_data = response.json()
                    return cart_data.get("items", [])
        except Exception as e:
            print(f"Error fetching cart items: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Não foi possível acessar o carrinho"
            )
        return []
    
    async def _verify_payment(self, pagamento_id: int) -> bool:
        """
        Verify payment status from payment service
        
        Args:
            pagamento_id: Payment ID
            
        Returns:
            True if payment is confirmed, False otherwise
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.payment_service_url}/pagamentos/{pagamento_id}",
                    timeout=5.0
                )
                if response.status_code == 200:
                    payment_data = response.json()
                    return payment_data.get("status") == "confirmado"
        except Exception as e:
            print(f"Error verifying payment: {e}")
        return False
    
    async def _calculate_shipping(self, endereco_id: int, peso_total: float) -> Dict[str, Any]:
        """
        Calculate shipping from shipping service
        
        Args:
            endereco_id: Address ID
            peso_total: Total weight
            
        Returns:
            Shipping details dictionary
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.shipping_service_url}/frete/calcular",
                    json={"endereco_id": endereco_id, "peso_total": peso_total},
                    timeout=5.0
                )
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Error calculating shipping: {e}")
        return {"valor": 0, "prazo_dias": 7}
    
    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new order
        
        Args:
            order_data: Order data including items
            
        Returns:
            Created order data
            
        Raises:
            HTTPException: If creation fails
        """
        # Extract items
        items_data = order_data.pop("items", [])
        
        if not items_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pedido deve ter pelo menos um item"
            )
        
        # Calculate total
        valor_total = sum(
            item["preco_unitario"] * item["quantidade"]
            for item in items_data
        )
        valor_total += order_data.get("valor_frete", 0)
        
        # Generate order number
        last_order_number = self.order_repo.get_last_order_number()
        numero_pedido = self.order_number_service.generate_order_number(last_order_number)
        
        # Ensure unique order number
        while self.order_repo.numero_pedido_exists(numero_pedido):
            numero_pedido = self.order_number_service.generate_order_number(numero_pedido)
        
        # Calculate estimated delivery date
        prazo_dias = 7  # Default
        data_entrega_prevista = datetime.now() + timedelta(days=prazo_dias)
        
        # Prepare order data
        order_create_data = {
            **order_data,
            "numero_pedido": numero_pedido,
            "valor_total": valor_total,
            "status": StatusPedido.PENDENTE,
            "data_entrega_prevista": data_entrega_prevista
        }
        
        # Create order with items
        order = self.order_repo.create_order(order_create_data, items_data)
        
        return self._serialize_order(order, include_details=True)
    
    async def create_order_from_cart(
        self,
        usuario_id: int,
        endereco_entrega_id: int,
        pagamento_id: int,
        observacoes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create order from cart after payment confirmation
        
        Args:
            usuario_id: User ID
            endereco_entrega_id: Delivery address ID
            pagamento_id: Payment ID
            observacoes: Optional observations
            
        Returns:
            Created order data
            
        Raises:
            HTTPException: If creation fails
        """
        # Verify payment
        payment_confirmed = await self._verify_payment(pagamento_id)
        if not payment_confirmed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Pagamento não confirmado"
            )
        
        # Fetch cart items
        cart_items = await self._fetch_cart_items(usuario_id)
        if not cart_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Carrinho vazio"
            )
        
        # Convert cart items to order items
        items_data = []
        for cart_item in cart_items:
            items_data.append({
                "livro_id": cart_item["livro_id"],
                "quantidade": cart_item["quantidade"],
                "preco_unitario": cart_item["preco_unitario"]
            })
        
        # Calculate shipping
        peso_total = len(cart_items) * 0.5  # Estimate 0.5kg per book
        shipping_info = await self._calculate_shipping(endereco_entrega_id, peso_total)
        
        # Create order
        order_data = {
            "usuario_id": usuario_id,
            "endereco_entrega_id": endereco_entrega_id,
            "valor_frete": shipping_info.get("valor", 0),
            "observacoes": observacoes,
            "items": items_data
        }
        
        return self.create_order(order_data)
    
    def get_order_by_id(self, order_id: int) -> Dict[str, Any]:
        """
        Get order by ID
        
        Args:
            order_id: Order ID
            
        Returns:
            Order data
            
        Raises:
            HTTPException: If not found
        """
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido não encontrado"
            )
        
        return self._serialize_order(order, include_details=True)
    
    def get_order_by_numero(self, numero_pedido: str) -> Dict[str, Any]:
        """
        Get order by order number
        
        Args:
            numero_pedido: Order number
            
        Returns:
            Order data
            
        Raises:
            HTTPException: If not found
        """
        order = self.order_repo.get_by_numero_pedido(numero_pedido)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido não encontrado"
            )
        
        return self._serialize_order(order, include_details=True)
    
    def get_user_orders(
        self,
        usuario_id: int,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get user order history with pagination
        
        Args:
            usuario_id: User ID
            page: Page number
            page_size: Items per page
            status: Optional status filter
            
        Returns:
            Dictionary with orders list and pagination info
        """
        # Convert status string to enum if provided
        status_enum = None
        if status:
            try:
                status_enum = StatusPedido(status)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Status inválido: {status}"
                )
        
        skip = (page - 1) * page_size
        
        orders, total = self.order_repo.get_by_usuario(
            usuario_id=usuario_id,
            skip=skip,
            limit=page_size,
            status=status_enum
        )
        
        # Serialize orders
        orders_data = [self._serialize_order(order) for order in orders]
        
        # Calculate pagination info
        total_pages = (total + page_size - 1) // page_size
        
        return {
            "items": orders_data,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1
        }
    
    def update_order_status(self, order_id: int, status: str) -> Dict[str, Any]:
        """
        Update order status
        
        Args:
            order_id: Order ID
            status: New status
            
        Returns:
            Updated order data
            
        Raises:
            HTTPException: If update fails
        """
        # Convert status string to enum
        try:
            status_enum = StatusPedido(status)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Status inválido: {status}"
            )
        
        order = self.order_repo.update_status(order_id, status_enum)
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido não encontrado"
            )
        
        return self._serialize_order(order, include_details=True)
    
    def get_all_orders(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
        usuario_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get all orders with pagination (Admin)
        
        Args:
            page: Page number
            page_size: Items per page
            status: Optional status filter
            
        Returns:
            Dictionary with orders list and pagination info
        """
        # Convert status string to enum if provided
        status_enum = None
        if status:
            try:
                status_enum = StatusPedido(status)
            except ValueError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Status inválido: {status}"
                )
        
        skip = (page - 1) * page_size
        
        orders, total = self.order_repo.get_all(
            skip=skip,
            limit=page_size,
            status=status_enum,
            usuario_id=usuario_id
        )
        
        # Serialize orders
        orders_data = [self._serialize_order(order) for order in orders]
        
        # Calculate pagination info
        total_pages = (total + page_size - 1) // page_size
        
        return {
            "items": orders_data,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1
        }
