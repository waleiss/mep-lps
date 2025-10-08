# Payment Service - Mundo em Palavras
# Microserviço responsável pelo processamento de pagamentos
# Gerencia transações, métodos de pagamento e confirmações

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Configuração da aplicação FastAPI
app = FastAPI(
    title="Payment Service",
    description="Microserviço de processamento de pagamentos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Modelos Pydantic
class PaymentRequest(BaseModel):
    amount: float
    currency: str = "BRL"
    payment_method: str
    order_id: str
    customer_id: str

class PaymentResponse(BaseModel):
    payment_id: str
    status: str
    amount: float
    currency: str
    transaction_id: Optional[str] = None

class PaymentStatus(BaseModel):
    payment_id: str
    status: str
    amount: float
    created_at: str

# Rotas básicas
@app.get("/")
async def root():
    """Endpoint raiz do serviço de pagamento"""
    return {
        "service": "Payment Service",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check do serviço"""
    return {"status": "healthy", "service": "payment"}

@app.post("/process", response_model=PaymentResponse)
async def process_payment(payment: PaymentRequest):
    """Processar pagamento"""
    # TODO: Integrar com gateways de pagamento reais (Stripe, PagSeguro, etc.)
    
    # Mock de processamento
    payment_id = f"pay_{len(payment.order_id)}_{payment.amount}"
    
    # Simular diferentes status baseado no valor
    if payment.amount > 1000:
        status = "failed"
    else:
        status = "completed"
    
    return PaymentResponse(
        payment_id=payment_id,
        status=status,
        amount=payment.amount,
        currency=payment.currency,
        transaction_id=f"txn_{payment_id}" if status == "completed" else None
    )

@app.get("/payment/{payment_id}", response_model=PaymentStatus)
async def get_payment_status(payment_id: str):
    """Obter status do pagamento"""
    # TODO: Buscar status real do gateway
    return PaymentStatus(
        payment_id=payment_id,
        status="completed",
        amount=99.90,
        created_at="2025-10-08T20:00:00Z"
    )

@app.post("/refund/{payment_id}")
async def refund_payment(payment_id: str, amount: Optional[float] = None):
    """Processar estorno"""
    # TODO: Implementar lógica de estorno
    return {
        "payment_id": payment_id,
        "refund_id": f"ref_{payment_id}",
        "status": "refunded",
        "amount": amount or 99.90
    }

@app.get("/methods")
async def get_payment_methods():
    """Listar métodos de pagamento disponíveis"""
    return {
        "methods": [
            {
                "id": "credit_card",
                "name": "Cartão de Crédito",
                "enabled": True
            },
            {
                "id": "pix",
                "name": "PIX",
                "enabled": True
            },
            {
                "id": "boleto",
                "name": "Boleto Bancário",
                "enabled": True
            }
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)