# Configuration management for Shipping Service
# Centralizes all configuration settings and environment variables

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Database
    database_url: str = "postgresql://admin:admin1234@localhost:5437/mundo_palavras_shipping"
    
    # CORS Configuration
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://localhost:8000"]
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # API Configuration
    api_prefix: str = "/api/v1"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    
    # Service URLs (for inter-service communication)
    auth_service_url: str = "http://localhost:8001"
    catalog_service_url: str = "http://localhost:8002"
    cart_service_url: str = "http://localhost:8003"
    order_service_url: str = "http://localhost:8006"
    
    # Shipping Configuration
    frete_economico_valor: float = 15.00
    frete_economico_prazo: int = 10
    frete_gratis_valor: float = 0.00
    frete_gratis_prazo: int = 20
    peso_maximo_kg: float = 30.0
    
    # External APIs
    viacep_base_url: str = "https://viacep.com.br/ws"
    viacep_timeout: float = 5.0
    
    # Correios API (opcional, para integração futura)
    correios_api_url: str = "https://api.correios.com.br"
    correios_api_key: str = "your-correios-api-key"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

