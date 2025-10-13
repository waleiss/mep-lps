# Redis Service - Cart session caching
# Handles Redis operations for cart data caching

import json
import redis
from typing import Optional, Dict, Any
from decimal import Decimal

from config import settings


class RedisService:
    """Service for Redis cache operations"""
    
    def __init__(self):
        """Initialize Redis connection"""
        try:
            self.redis_client = redis.from_url(
                settings.redis_url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test connection
            self.redis_client.ping()
        except redis.ConnectionError as e:
            print(f"Warning: Could not connect to Redis: {e}")
            self.redis_client = None
    
    def _get_cart_key(self, usuario_id: int) -> str:
        """Generate Redis key for cart"""
        return f"cart:user:{usuario_id}"
    
    def get_cart(self, usuario_id: int) -> Optional[Dict[str, Any]]:
        """
        Get cart data from Redis cache
        
        Args:
            usuario_id: User ID
            
        Returns:
            Cart data dictionary or None if not found
        """
        if not self.redis_client:
            return None
        
        try:
            key = self._get_cart_key(usuario_id)
            data = self.redis_client.get(key)
            
            if data:
                cart_data = json.loads(data)
                # Convert string Decimals back to Decimal objects
                if 'itens' in cart_data:
                    for item in cart_data['itens']:
                        if 'preco_unitario' in item:
                            item['preco_unitario'] = Decimal(str(item['preco_unitario']))
                        if 'subtotal' in item:
                            item['subtotal'] = Decimal(str(item['subtotal']))
                if 'valor_total' in cart_data:
                    cart_data['valor_total'] = Decimal(str(cart_data['valor_total']))
                return cart_data
            
            return None
            
        except Exception as e:
            print(f"Error getting cart from Redis: {e}")
            return None
    
    def set_cart(self, usuario_id: int, cart_data: Dict[str, Any]) -> bool:
        """
        Save cart data to Redis cache
        
        Args:
            usuario_id: User ID
            cart_data: Cart data dictionary
            
        Returns:
            True if successful, False otherwise
        """
        if not self.redis_client:
            return False
        
        try:
            key = self._get_cart_key(usuario_id)
            
            # Convert Decimal objects to strings for JSON serialization
            cart_copy = cart_data.copy()
            if 'itens' in cart_copy:
                for item in cart_copy['itens']:
                    if 'preco_unitario' in item and isinstance(item['preco_unitario'], Decimal):
                        item['preco_unitario'] = str(item['preco_unitario'])
                    if 'subtotal' in item and isinstance(item['subtotal'], Decimal):
                        item['subtotal'] = str(item['subtotal'])
            if 'valor_total' in cart_copy and isinstance(cart_copy['valor_total'], Decimal):
                cart_copy['valor_total'] = str(cart_copy['valor_total'])
            
            # Serialize to JSON and save with TTL
            json_data = json.dumps(cart_copy, default=str)
            self.redis_client.setex(
                key,
                settings.redis_ttl,
                json_data
            )
            return True
            
        except Exception as e:
            print(f"Error saving cart to Redis: {e}")
            return False
    
    def delete_cart(self, usuario_id: int) -> bool:
        """
        Delete cart from Redis cache
        
        Args:
            usuario_id: User ID
            
        Returns:
            True if successful, False otherwise
        """
        if not self.redis_client:
            return False
        
        try:
            key = self._get_cart_key(usuario_id)
            self.redis_client.delete(key)
            return True
            
        except Exception as e:
            print(f"Error deleting cart from Redis: {e}")
            return False
    
    def refresh_ttl(self, usuario_id: int) -> bool:
        """
        Refresh TTL for cart in Redis
        
        Args:
            usuario_id: User ID
            
        Returns:
            True if successful, False otherwise
        """
        if not self.redis_client:
            return False
        
        try:
            key = self._get_cart_key(usuario_id)
            self.redis_client.expire(key, settings.redis_ttl)
            return True
            
        except Exception as e:
            print(f"Error refreshing cart TTL: {e}")
            return False
    
    def is_connected(self) -> bool:
        """Check if Redis is connected"""
        if not self.redis_client:
            return False
        
        try:
            self.redis_client.ping()
            return True
        except:
            return False


# Global Redis service instance
redis_service = RedisService()
