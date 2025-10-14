# Catalog Service - Mundo em Palavras
# Microserviço responsável pelo catálogo de livros
# Implementa arquitetura limpa com separação de responsabilidades

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import settings
from database import create_tables
from routes import router


# Create FastAPI application
app = FastAPI(
    title="Catalog Service",
    description="Microserviço de catálogo de livros - Mundo em Palavras",
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
    print("Catalog Service started successfully!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    print("Catalog Service shutting down...")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Catalog Service",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "catalog"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        reload=settings.debug
    )
