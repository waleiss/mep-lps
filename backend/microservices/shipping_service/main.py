# Shipping Service - Mundo em Palavras
# Microserviço responsável pelo cálculo de frete e envio
# Gerencia cotações, prazos e rastreamento

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

# Configuração da aplicação FastAPI
app = FastAPI(
    title="Shipping Service",
    description="Microserviço de cálculo de frete e envio",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Modelos Pydantic
class ShippingQuote(BaseModel):
    carrier: str
    service: str
    price: float
    estimated_days: int

class ShippingRequest(BaseModel):
    zip_code: str
    items: List[dict]  # Lista de itens com peso e dimensões

class ShippingResponse(BaseModel):
    quotes: List[ShippingQuote]
    total_weight: float

# Rotas básicas
@app.get("/")
async def root():
    """Endpoint raiz do serviço de frete"""
    return {
        "service": "Shipping Service",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check do serviço"""
    return {"status": "healthy", "service": "shipping"}

@app.post("/quote", response_model=ShippingResponse)
async def calculate_shipping(request: ShippingRequest):
    """Calcular cotações de frete"""
    # TODO: Integrar com APIs de transportadoras reais
    # Mock de cotações para demonstração
    
    quotes = [
        ShippingQuote(
            carrier="Correios",
            service="PAC",
            price=15.50,
            estimated_days=5
        ),
        ShippingQuote(
            carrier="Correios",
            service="SEDEX",
            price=25.90,
            estimated_days=2
        ),
        ShippingQuote(
            carrier="Transportadora ABC",
            service="Expresso",
            price=18.75,
            estimated_days=3
        )
    ]
    
    # Calcular peso total (mock)
    total_weight = sum(item.get("weight", 0.5) for item in request.items)
    
    return ShippingResponse(
        quotes=quotes,
        total_weight=total_weight
    )

@app.get("/tracking/{tracking_code}")
async def track_shipment(tracking_code: str):
    """Rastrear envio"""
    # TODO: Integrar com APIs de rastreamento
    return {
        "tracking_code": tracking_code,
        "status": "Em trânsito",
        "location": "Centro de Distribuição SP",
        "estimated_delivery": "2025-10-12"
    }

@app.get("/carriers")
async def get_carriers():
    """Listar transportadoras disponíveis"""
    return {
        "carriers": [
            {"id": "correios", "name": "Correios", "active": True},
            {"id": "abc", "name": "Transportadora ABC", "active": True},
            {"id": "xyz", "name": "Logística XYZ", "active": False}
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)