# Authentication Schemas - Pydantic models for request/response validation
# Defines data models for authentication endpoints

from typing import Optional
from pydantic import BaseModel, EmailStr, validator


class UserLoginRequest(BaseModel):
    """Request schema for user login"""
    email: EmailStr
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Password cannot be empty')
        return v.strip()


class UserRegisterRequest(BaseModel):
    """Request schema for user registration"""
    email: EmailStr
    password: str
    password_confirmation: str
    name: str
    
    @validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip()
    
    @validator('password')
    def validate_password(cls, v):
        if not v or len(v.strip()) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v.strip()
    
    @validator('password_confirmation')
    def validate_password_confirmation(cls, v, values):
        if not v or len(v.strip()) == 0:
            raise ValueError('Password confirmation cannot be empty')
        if 'password' in values and v.strip() != values['password']:
            raise ValueError('As senhas não coincidem')
        return v.strip()


class UserResponse(BaseModel):
    """Response schema for user data"""
    user_id: int
    email: str
    nome: str
    tipo: str
    ativo: bool


class LoginResponse(BaseModel):
    """Response schema for login endpoint"""
    user_id: int
    email: str
    nome: str
    tipo: str
    ativo: bool
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RegisterResponse(BaseModel):
    """Response schema for register endpoint"""
    user_id: int
    email: str
    nome: str
    tipo: str
    ativo: bool
    access_token: str
    refresh_token: str
    token_type: str = "bearer"