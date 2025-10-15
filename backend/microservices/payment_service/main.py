# Payment Service - Mundo em Palavras
# Microserviço responsável pelo processamento de pagamentos
# Implementa arquitetura limpa com separação de responsabilidades

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import settings
from database import create_tables
from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    # Startup
    create_tables()
    print("=" * 60)
    print("Payment Service started successfully!")
    print(f"API Docs: http://localhost:8005{settings.docs_url}")
    print(f"Version: 2.0.0")
    print(f"Environment: {settings.environment}")
    print("=" * 60)
    print("\nFeatures disponiveis:")
    print("  - Pagamento com cartao de credito/debito")
    print("  - Geracao de PIX (QR Code)")
    print("  - Geracao de boleto bancario")
    print("  - Consulta de status de pagamento")
    print("  - Logs de transacao completos")
    print("  - Simulacao de gateway de pagamento")
    print("=" * 60)
    
    yield
    
    # Shutdown
    print("\nPayment Service shutting down...")


# Create FastAPI application
app = FastAPI(
    title="Payment Service",
    description="Microserviço de processamento de pagamentos - Mundo em Palavras",
    version="2.0.0",
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix=settings.api_prefix)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8005,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug"
    )
