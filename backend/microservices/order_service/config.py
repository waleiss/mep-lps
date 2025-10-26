# Configuration management for Order Service
# Centralizes all configuration settings and environment variables

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Database
    database_url: str = "postgresql://admin:admin1234@localhost:5435/mundo_palavras_orders"
    
    # CORS Configuration
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # API Configuration
    api_prefix: str = "/api/v1"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    
    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100
    
    # External Services URLs
    auth_service_url: str = "http://auth-service:8001/api/v1"
    catalog_service_url: str = "http://catalog-service:8002/api/v1"
    cart_service_url: str = "http://cart-service:8003/api/v1"
    payment_service_url: str = "http://payment-service:8005/api/v1"
    shipping_service_url: str = "http://shipping-service:8004/api/v1"
    
    # Order Number Configuration
    order_number_prefix: str = "MP"  # Mundo em Palavras
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
