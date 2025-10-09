# User Service - Business logic for user operations
# Handles user registration, authentication, and profile management

from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from models import Usuario, TipoUsuario
from repositories.user_repository import UserRepository
from services.password_service import password_service
from services.jwt_service import jwt_service


class UserService:
    """Service for user business logic operations"""
    
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.password_service = password_service
        self.jwt_service = jwt_service
    
    def register_user(self, email: str, password: str, name: str) -> Dict[str, Any]:
        """
        Register a new user
        
        Args:
            email: User email
            password: User password
            name: User name
            
        Returns:
            Dictionary with user data and tokens
            
        Raises:
            HTTPException: If registration fails
        """
        # Check if email already exists
        if self.user_repo.email_exists(email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já cadastrado"
            )
        
        # Validate password strength
        if not self.password_service.is_password_strong(password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Senha deve ter pelo menos 8 caracteres, incluindo maiúscula, minúscula, número e caractere especial"
            )
        
        # Hash password
        hashed_password = self.password_service.hash_password(password)
        
        # Create user data
        user_data = {
            "nome": name,
            "email": email,
            "senha_hash": hashed_password,
            "tipo": TipoUsuario.CLIENTE,
            "ativo": True
        }
        
        # Create user
        user = self.user_repo.create(user_data)
        
        # Generate tokens
        tokens = self.jwt_service.create_token_pair(user.id, user.email)
        
        return {
            "user_id": user.id,
            "email": user.email,
            "nome": user.nome,
            "tipo": user.tipo.value,
            "ativo": user.ativo,
            **tokens
        }
    
    def authenticate_user(self, email: str, password: str) -> Optional[Usuario]:
        """
        Authenticate user with email and password
        
        Args:
            email: User email
            password: User password
            
        Returns:
            User instance if authentication successful, None otherwise
        """
        user = self.user_repo.get_by_email_and_active(email)
        if not user:
            return None
        
        if not self.password_service.verify_password(password, user.senha_hash):
            return None
        
        return user
    
    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """
        Login user and return tokens
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Dictionary with user data and tokens
            
        Raises:
            HTTPException: If login fails
        """
        user = self.authenticate_user(email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou senha incorretos",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Generate tokens
        tokens = self.jwt_service.create_token_pair(user.id, user.email)
        
        return {
            "user_id": user.id,
            "email": user.email,
            "nome": user.nome,
            "tipo": user.tipo.value,
            "ativo": user.ativo,
            **tokens
        }
    
