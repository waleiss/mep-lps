# Mundo em Palavras - Auth Service
# Microserviço responsável pela autenticação e autorização de usuários
# Implementa arquitetura limpa com separação de responsabilidades

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import settings
from database import create_tables
from routes import router


# Create FastAPI application
app = FastAPI(
    title="Mundo em Palavras",
    description="Microserviço de autenticação e autorização - Mundo em Palavras",
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
    print("Mundo em Palavras - Auth Service started successfully!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    print("Mundo em Palavras - Auth Service shutting down...")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug"
    )