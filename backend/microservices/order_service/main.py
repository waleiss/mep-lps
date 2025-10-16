# Order Service - Mundo em Palavras
# Microserviço responsável pelo gerenciamento de pedidos
# Implementa arquitetura limpa com separação de responsabilidades

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import settings
from database import create_tables
from routes import router


# Create FastAPI application
app = FastAPI(
    title="Order Service",
    description="Microserviço de gerenciamento de pedidos - Mundo em Palavras",
    version="1.0.0",
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url
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


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    # Create database tables
    create_tables()
    print("Order Service started successfully!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    print("Order Service shutting down...")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Order Service",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "order"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8006,
        reload=settings.debug
    )
