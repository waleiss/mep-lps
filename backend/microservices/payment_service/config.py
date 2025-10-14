# Configuration management for Payment Service
# Centralizes all configuration settings and environment variables

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Database
    database_url: str = "postgresql://admin:admin1234@localhost:5436/mundo_palavras_payments"
    
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
    order_service_url: str = "http://localhost:8006"
    
    # Payment Gateway Configuration (mock)
    payment_gateway_url: str = "https://api.payment-gateway.com"
    payment_gateway_key: str = "mock-gateway-key"
    
    # Stripe Configuration (para integração futura)
    stripe_secret_key: str = "sk_test_your_stripe_secret_key"
    stripe_publishable_key: str = "pk_test_your_stripe_publishable_key"
    
    # Payment Settings
    max_parcelas: int = 12
    pix_validade_minutos: int = 30
    boleto_vencimento_dias: int = 3
    
    # Security
    encrypt_card_data: bool = True
    log_sensitive_data: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

