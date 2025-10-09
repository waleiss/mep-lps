# Authentication Middleware - JWT token validation and user extraction
# Handles authentication for protected endpoints

from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from database import get_db
from models import Usuario
from repositories.user_repository import UserRepository
from services.jwt_service import jwt_service


# Security scheme
security = HTTPBearer()


class AuthMiddleware:
    """Authentication middleware for JWT token validation"""
    
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.jwt_service = jwt_service
    
    def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> Usuario:
        """
        Get current authenticated user from JWT token
        
        Args:
            credentials: HTTP Bearer credentials
            
        Returns:
            Current authenticated user
            
        Raises:
            HTTPException: If authentication fails
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        try:
            # Verify and decode token
            payload = self.jwt_service.verify_token(credentials.credentials)
            
            # Extract user information
            email: str = payload.get("sub")
            user_id: int = payload.get("user_id")
            
            if email is None or user_id is None:
                raise credentials_exception
            
        except HTTPException:
            raise
        except Exception:
            raise credentials_exception
        
        # Get user from database
        user = self.user_repo.get_by_id(user_id)
        if user is None or not user.ativo:
            raise credentials_exception
        
        return user
    
    def get_current_active_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> Usuario:
        """
        Get current active user from JWT token
        
        Args:
            credentials: HTTP Bearer credentials
            
        Returns:
            Current active user
            
        Raises:
            HTTPException: If authentication fails or user is inactive
        """
        user = self.get_current_user(credentials)
        
        if not user.ativo:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Inactive user"
            )
        
        return user
    
    def get_optional_current_user(self, credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[Usuario]:
        """
        Get current user if token is provided, otherwise return None
        
        Args:
            credentials: Optional HTTP Bearer credentials
            
        Returns:
            Current user or None
        """
        if not credentials:
            return None
        
        try:
            return self.get_current_user(credentials)
        except HTTPException:
            return None


# Dependency functions for FastAPI
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), 
                    db: Session = Depends(get_db)) -> Usuario:
    """FastAPI dependency to get current authenticated user"""
    auth_middleware = AuthMiddleware(db)
    return auth_middleware.get_current_user(credentials)


def get_current_active_user(credentials: HTTPAuthorizationCredentials = Depends(security), 
                           db: Session = Depends(get_db)) -> Usuario:
    """FastAPI dependency to get current active user"""
    auth_middleware = AuthMiddleware(db)
    return auth_middleware.get_current_active_user(credentials)


def get_optional_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security), 
                             db: Session = Depends(get_db)) -> Optional[Usuario]:
    """FastAPI dependency to get current user if authenticated, otherwise None"""
    auth_middleware = AuthMiddleware(db)
    return auth_middleware.get_optional_current_user(credentials)
