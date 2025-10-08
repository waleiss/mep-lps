# Auth Service - Mundo em Palavras
# Microserviço responsável pela autenticação e autorização de usuários
# Gerencia login, registro, tokens JWT e permissões

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional
import uvicorn

# Configuração da aplicação FastAPI
app = FastAPI(
    title="Auth Service",
    description="Microserviço de autenticação e autorização",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Modelos Pydantic
class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(BaseModel):
    email: str
    password: str
    name: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

# Security
security = HTTPBearer()

# Rotas básicas
@app.get("/")
async def root():
    """Endpoint raiz do serviço de autenticação"""
    return {
        "service": "Auth Service",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check do serviço"""
    return {"status": "healthy", "service": "auth"}

@app.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin):
    """Endpoint de login de usuário"""
    # TODO: Implementar lógica de autenticação
    return {
        "access_token": "fake-jwt-token",
        "token_type": "bearer"
    }

@app.post("/register")
async def register(user_data: UserRegister):
    """Endpoint de registro de usuário"""
    # TODO: Implementar lógica de registro
    return {"message": "User registered successfully"}

@app.get("/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Endpoint para obter dados do usuário atual"""
    # TODO: Implementar validação de token
    return {"user_id": "123", "email": "user@example.com"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)