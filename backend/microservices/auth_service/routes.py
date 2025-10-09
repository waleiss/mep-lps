# Authentication Routes - Basic endpoints
# Implements /register, /login and authentication middleware

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from services.user_service import UserService
from middleware.auth_middleware import get_current_active_user
from schemas.auth_schemas import (
    UserLoginRequest,
    UserRegisterRequest,
    LoginResponse,
    RegisterResponse,
    UserResponse
)
from models import Usuario

# Create router
router = APIRouter()


# Health endpoints
@router.get("/")
async def root():
    """Endpoint raiz do serviço de autenticação"""
    return {
        "service": "Auth Service",
        "status": "running",
        "version": "1.0.0"
    }


@router.get("/health")
async def health_check():
    """Health check do serviço"""
    return {"status": "healthy", "service": "auth"}


# Authentication endpoints
@router.post("/register", response_model=RegisterResponse)
async def register_user(
    user_data: UserRegisterRequest,
    db: Session = Depends(get_db)
):
    """Endpoint de registro de usuário"""
    user_service = UserService(db)
    
    try:
        result = user_service.register_user(
            email=user_data.email,
            password=user_data.password,
            name=user_data.name
        )
        
        return RegisterResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )


@router.post("/login", response_model=LoginResponse)
async def login_user(
    user_data: UserLoginRequest,
    db: Session = Depends(get_db)
):
    """Endpoint de login de usuário"""
    user_service = UserService(db)
    
    try:
        result = user_service.login_user(
            email=user_data.email,
            password=user_data.password
        )
        
        return LoginResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: Usuario = Depends(get_current_active_user)
):
    """Endpoint para obter dados do usuário atual"""
    return {
        "user_id": current_user.id,
        "email": current_user.email,
        "nome": current_user.nome,
        "tipo": current_user.tipo.value if current_user.tipo else None,
        "ativo": current_user.ativo
    }