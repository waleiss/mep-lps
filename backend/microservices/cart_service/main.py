# Cart Service - Mundo em Palavras
# Microserviço responsável pelo carrinho de compras
# Gerencia itens do carrinho, adição/remoção de produtos

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# Configuração da aplicação FastAPI
app = FastAPI(
    title="Cart Service",
    description="Microserviço de carrinho de compras",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Modelos Pydantic
class CartItem(BaseModel):
    book_id: str
    title: str
    price: float
    quantity: int

class Cart(BaseModel):
    user_id: str
    items: List[CartItem]
    total: float

class AddToCartRequest(BaseModel):
    book_id: str
    quantity: int = 1

# Dados mock para demonstração
carts_db = {}

# Rotas básicas
@app.get("/")
async def root():
    """Endpoint raiz do serviço de carrinho"""
    return {
        "service": "Cart Service",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check do serviço"""
    return {"status": "healthy", "service": "cart"}

@app.get("/cart/{user_id}", response_model=Cart)
async def get_cart(user_id: str):
    """Obter carrinho do usuário"""
    cart = carts_db.get(user_id, Cart(user_id=user_id, items=[], total=0.0))
    return cart

@app.post("/cart/{user_id}/add")
async def add_to_cart(user_id: str, item: AddToCartRequest):
    """Adicionar item ao carrinho"""
    if user_id not in carts_db:
        carts_db[user_id] = Cart(user_id=user_id, items=[], total=0.0)
    
    cart = carts_db[user_id]
    
    # Verificar se o item já existe no carrinho
    existing_item = next((i for i in cart.items if i.book_id == item.book_id), None)
    
    if existing_item:
        existing_item.quantity += item.quantity
    else:
        # TODO: Buscar dados do livro no catalog service
        new_item = CartItem(
            book_id=item.book_id,
            title=f"Livro {item.book_id}",
            price=29.90,  # Mock price
            quantity=item.quantity
        )
        cart.items.append(new_item)
    
    # Recalcular total
    cart.total = sum(item.price * item.quantity for item in cart.items)
    
    return {"message": "Item added to cart", "cart": cart}

@app.delete("/cart/{user_id}/items/{book_id}")
async def remove_from_cart(user_id: str, book_id: str):
    """Remover item do carrinho"""
    if user_id not in carts_db:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    cart = carts_db[user_id]
    cart.items = [item for item in cart.items if item.book_id != book_id]
    
    # Recalcular total
    cart.total = sum(item.price * item.quantity for item in cart.items)
    
    return {"message": "Item removed from cart", "cart": cart}

@app.delete("/cart/{user_id}")
async def clear_cart(user_id: str):
    """Limpar carrinho"""
    if user_id in carts_db:
        carts_db[user_id] = Cart(user_id=user_id, items=[], total=0.0)
    
    return {"message": "Cart cleared"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)