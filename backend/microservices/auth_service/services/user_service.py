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
        
        # Detectar tipo de usuário baseado no email
        # Se email contém @admin, define como ADMIN
        user_type = TipoUsuario.ADMIN if "@admin" in email.lower() else TipoUsuario.CLIENTE
        
        # Create user data
        user_data = {
            "nome": name,
            "email": email,
            "senha_hash": hashed_password,
            "tipo": user_type,
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
    
    def get_user_by_id(self, user_id: int) -> Optional[Usuario]:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User instance or None if not found
        """
        return self.user_repo.get_by_id(user_id)

    def update_user(self, user_id: int, telefone: Optional[str] = None, email: Optional[str] = None, nome: Optional[str] = None) -> Usuario:
        """Atualiza dados simples do usuário (ex.: telefone, email, nome)."""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

        update_data = {}
        if telefone is not None:
            update_data["telefone"] = telefone
        if email is not None:
            new_email = email.strip().lower()
            if new_email != user.email:
                # verifica duplicidade
                if self.user_repo.email_exists(new_email):
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")
                update_data["email"] = new_email
        if nome is not None:
            new_name = nome.strip()
            if len(new_name) < 2:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nome deve ter pelo menos 2 caracteres")
            update_data["nome"] = new_name
        if not update_data:
            return user
        updated = self.user_repo.update(user_id, update_data)
        if not updated:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")
        return updated

    def change_password(self, user_id: int, current_password: str, new_password: str, new_password_confirmation: str) -> None:
        """Troca a senha do usuário com verificação da senha atual."""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

        # Verifica senha atual
        if not self.password_service.verify_password(current_password, user.senha_hash):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Senha atual incorreta")

        if new_password != new_password_confirmation:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="As senhas não coincidem")

        if not self.password_service.is_password_strong(new_password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Senha não atende aos requisitos de segurança")

        user.senha_hash = self.password_service.hash_password(new_password)
        self.user_repo.db.commit()
    
