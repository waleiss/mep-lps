# Shipping Service - Mundo em Palavras
# Microserviço responsável pelo cálculo de frete, endereços e envio
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
    print("Shipping Service started successfully!")
    print(f"API Docs: http://localhost:8004{settings.docs_url}")
    print(f"Version: 2.0.0")
    print(f"Environment: {settings.environment}")
    print("=" * 60)
    print("\nFeatures disponiveis:")
    print("  - Calculo de frete (R$ 15,00/10 dias ou Gratis/20 dias)")
    print("  - Gerenciamento de enderecos de usuarios")
    print("  - Validacao de CEP via ViaCEP")
    print("  - CRUD completo de enderecos")
    print("=" * 60)
    
    yield
    
    # Shutdown
    print("\nShipping Service shutting down...")


# Create FastAPI application
app = FastAPI(
    title="Shipping Service",
    description="Microserviço de frete e endereços - Mundo em Palavras",
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
        port=8004,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug"
    )
