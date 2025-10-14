# JWT Service - Token generation and validation
# Handles JWT token creation, validation, and refresh token management

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from fastapi import HTTPException, status

from config import settings


class JWTService:
    """Service for JWT token operations"""
    
    def __init__(self):
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.access_token_expire_minutes = settings.access_token_expire_minutes
        self.refresh_token_expire_days = settings.refresh_token_expire_days
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token
        
        Args:
            data: Data to encode in the token
            expires_delta: Token expiration time
            
        Returns:
            Encoded JWT token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        # Convert to timestamp
        expire_timestamp = int(expire.timestamp())
        
        to_encode.update({
            "exp": expire_timestamp,
            "type": "access",
            "iat": int(datetime.utcnow().timestamp())
        })
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """
        Create a JWT refresh token
        
        Args:
            data: Data to encode in the token
            
        Returns:
            Encoded JWT refresh token
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        expire_timestamp = int(expire.timestamp())
        
        to_encode.update({
            "exp": expire_timestamp,
            "type": "refresh",
            "iat": int(datetime.utcnow().timestamp())
        })
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str, token_type: str = "access") -> Dict[str, Any]:
        """
        Verify and decode a JWT token
        
        Args:
            token: JWT token to verify
            token_type: Expected token type (access or refresh)
            
        Returns:
            Decoded token payload
            
        Raises:
            HTTPException: If token is invalid or expired
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            
            # Verify token type
            if payload.get("type") != token_type:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"Invalid token type. Expected {token_type}",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Check if token is expired
            exp = payload.get("exp")
            if exp and datetime.utcnow().timestamp() > exp:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return payload
            
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e
    
    def create_token_pair(self, user_id: int, email: str) -> Dict[str, str]:
        """
        Create both access and refresh tokens for a user
        
        Args:
            user_id: User ID
            email: User email
            
        Returns:
            Dictionary containing access_token and refresh_token
        """
        token_data = {
            "sub": email,
            "user_id": user_id
        }
        
        access_token = self.create_access_token(token_data)
        refresh_token = self.create_refresh_token(token_data)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    def refresh_access_token(self, refresh_token: str) -> str:
        """
        Create a new access token from a refresh token
        
        Args:
            refresh_token: Valid refresh token
            
        Returns:
            New access token
        """
        payload = self.verify_token(refresh_token, "refresh")
        
        token_data = {
            "sub": payload.get("sub"),
            "user_id": payload.get("user_id")
        }
        
        return self.create_access_token(token_data)


# Global JWT service instance
jwt_service = JWTService()
