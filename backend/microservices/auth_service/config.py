# Configuration management for Auth Service
# Centralizes all configuration settings and environment variables

import os
from typing import Optional
from pydantic import BaseModel, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Database
    database_url: str = "sqlite:///./auth_service.db"
    
    # JWT Configuration
    secret_key: str = "your-super-secret-jwt-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7
    
    # Password Hashing
    bcrypt_rounds: int = 12
    
    # Redis Configuration (for token blacklisting)
    redis_url: str = "redis://localhost:6379/0"
    
    # CORS Configuration
    allowed_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # API Configuration
    api_prefix: str = "/api/v1"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    
    @validator("secret_key")
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError("Secret key must be at least 32 characters long")
        return v
    
    @validator("bcrypt_rounds")
    def validate_bcrypt_rounds(cls, v):
        if v < 10 or v > 15:
            raise ValueError("BCrypt rounds must be between 10 and 15")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
