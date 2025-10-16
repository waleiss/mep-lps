# Configuration management for Recommendation Service
# Centralizes all configuration settings and environment variables

import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Database
    database_url: str = "postgresql://admin:admin1234@localhost:5438/mundo_palavras_recommendations"
    
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
    default_page_size: int = 10
    max_page_size: int = 50
    
    # External Services URLs
    catalog_service_url: str = "http://localhost:8002/api/v1"
    order_service_url: str = "http://localhost:8004/api/v1"
    
    # Recommendation Settings
    max_recommendations: int = 20
    similarity_threshold: float = 0.3
    cache_ttl: int = 1800  # 30 minutes
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
