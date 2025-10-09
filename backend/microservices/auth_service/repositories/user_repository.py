# User Repository - Data access layer for user operations
# Implements repository pattern for user data access

from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models import Usuario, TipoUsuario


class UserRepository:
    """Repository for user data operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user_data: dict) -> Usuario:
        """
        Create a new user
        
        Args:
            user_data: User data dictionary
            
        Returns:
            Created user instance
        """
        db_user = Usuario(**user_data)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    def get_by_id(self, user_id: int) -> Optional[Usuario]:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User instance or None if not found
        """
        return self.db.query(Usuario).filter(Usuario.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[Usuario]:
        """
        Get user by email
        
        Args:
            email: User email
            
        Returns:
            User instance or None if not found
        """
        return self.db.query(Usuario).filter(Usuario.email == email).first()
    
    def get_by_email_and_active(self, email: str) -> Optional[Usuario]:
        """
        Get active user by email
        
        Args:
            email: User email
            
        Returns:
            Active user instance or None if not found
        """
        return self.db.query(Usuario).filter(
            and_(Usuario.email == email, Usuario.ativo == True)
        ).first()
    
    def update(self, user_id: int, update_data: dict) -> Optional[Usuario]:
        """
        Update user data
        
        Args:
            user_id: User ID
            update_data: Dictionary with fields to update
            
        Returns:
            Updated user instance or None if not found
        """
        user = self.get_by_id(user_id)
        if not user:
            return None
        
        for field, value in update_data.items():
            if hasattr(user, field):
                setattr(user, field, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user_id: int) -> bool:
        """
        Soft delete user (set ativo = False)
        
        Args:
            user_id: User ID
            
        Returns:
            True if user was deleted, False if not found
        """
        user = self.get_by_id(user_id)
        if not user:
            return False
        
        user.ativo = False
        self.db.commit()
        return True
    
    def get_all_active(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """
        Get all active users with pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of active users
        """
        return self.db.query(Usuario).filter(
            Usuario.ativo == True
        ).offset(skip).limit(limit).all()
    
    def get_by_type(self, tipo: TipoUsuario, skip: int = 0, limit: int = 100) -> List[Usuario]:
        """
        Get users by type with pagination
        
        Args:
            tipo: User type
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of users of specified type
        """
        return self.db.query(Usuario).filter(
            and_(Usuario.tipo == tipo, Usuario.ativo == True)
        ).offset(skip).limit(limit).all()
    
    def email_exists(self, email: str) -> bool:
        """
        Check if email already exists
        
        Args:
            email: Email to check
            
        Returns:
            True if email exists, False otherwise
        """
        return self.db.query(Usuario).filter(Usuario.email == email).first() is not None
    
    def count_active_users(self) -> int:
        """
        Count total number of active users
        
        Returns:
            Number of active users
        """
        return self.db.query(Usuario).filter(Usuario.ativo == True).count()
