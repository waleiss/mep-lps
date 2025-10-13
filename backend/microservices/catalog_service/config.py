# Configuration management for Catalog Service
# Centralizes all configuration settings and environment variables

import os
from typing import List
from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Database
    database_url: str = "sqlite:///./catalog_service.db"
    
    # Redis Configuration (for caching)
    redis_url: str = "redis://localhost:6379/1"
    cache_ttl: int = 3600  # Cache TTL in seconds (1 hour)
    
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
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
