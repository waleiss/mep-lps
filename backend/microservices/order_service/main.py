# Order Service - Mundo em Palavras
# Microserviço responsável pelo gerenciamento de pedidos
# Gerencia criação, status e histórico de pedidos

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uvicorn

# Configuração da aplicação FastAPI
app = FastAPI(
    title="Order Service",
    description="Microserviço de gerenciamento de pedidos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Modelos Pydantic
class OrderItem(BaseModel):
    book_id: str
    title: str
    price: float
    quantity: int

class OrderCreate(BaseModel):
    user_id: str
    items: List[OrderItem]
    shipping_address: dict
    payment_method: str

class Order(BaseModel):
    order_id: str
    user_id: str
    items: List[OrderItem]
    total: float
    status: str
    created_at: datetime
    shipping_address: dict
    payment_method: str

# Dados mock para demonstração
orders_db = {}

# Rotas básicas
@app.get("/")
async def root():
    """Endpoint raiz do serviço de pedidos"""
    return {
        "service": "Order Service",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check do serviço"""
    return {"status": "healthy", "service": "order"}

@app.post("/orders", response_model=Order)
async def create_order(order_data: OrderCreate):
    """Criar novo pedido"""
    order_id = f"ORD_{len(orders_db) + 1:06d}"
    
    # Calcular total
    total = sum(item.price * item.quantity for item in order_data.items)
    
    order = Order(
        order_id=order_id,
        user_id=order_data.user_id,
        items=order_data.items,
        total=total,
        status="pending",
        created_at=datetime.now(),
        shipping_address=order_data.shipping_address,
        payment_method=order_data.payment_method
    )
    
    orders_db[order_id] = order
    
    return order

@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: str):
    """Obter detalhes de um pedido"""
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.get("/orders/user/{user_id}", response_model=List[Order])
async def get_user_orders(user_id: str):
    """Obter pedidos de um usuário"""
    user_orders = [order for order in orders_db.values() if order.user_id == user_id]
    return sorted(user_orders, key=lambda x: x.created_at, reverse=True)

@app.put("/orders/{order_id}/status")
async def update_order_status(order_id: str, status: str):
    """Atualizar status do pedido"""
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    valid_statuses = ["pending", "confirmed", "processing", "shipped", "delivered", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    order.status = status
    return {"message": "Order status updated", "order_id": order_id, "status": status}

@app.get("/orders/{order_id}/tracking")
async def get_order_tracking(order_id: str):
    """Obter informações de rastreamento do pedido"""
    order = orders_db.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # TODO: Integrar com shipping service para rastreamento real
    return {
        "order_id": order_id,
        "status": order.status,
        "tracking_code": f"TRK_{order_id}",
        "estimated_delivery": "2025-10-15"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8006)