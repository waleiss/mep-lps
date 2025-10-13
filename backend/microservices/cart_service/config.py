# Configuration management for Cart Service
# Centralizes all configuration settings and environment variables

import os
from typing import Optional
from pydantic import BaseModel, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Database
    database_url: str = "sqlite:///./cart_service.db"
    
    # Redis Configuration (for cart session caching)
    redis_url: str = "redis://localhost:6379/2"
    redis_ttl: int = 86400  # 24 hours in seconds
    
    # CORS Configuration
    allowed_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # API Configuration
    api_prefix: str = "/api/v1"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    
    # Service URLs (for inter-service communication)
    catalog_service_url: str = "http://localhost:8002"
    auth_service_url: str = "http://localhost:8001"
    
    # Cart Configuration
    max_quantity_per_item: int = 99
    cart_expiration_days: int = 30
    
    @validator("redis_ttl")
    def validate_redis_ttl(cls, v):
        if v < 3600:  # Minimum 1 hour
            raise ValueError("Redis TTL must be at least 3600 seconds (1 hour)")
        return v
    
    @validator("max_quantity_per_item")
    def validate_max_quantity(cls, v):
        if v < 1 or v > 999:
            raise ValueError("Max quantity per item must be between 1 and 999")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
