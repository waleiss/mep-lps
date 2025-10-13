# Cache Service - Redis caching for book data
# Implements caching strategy to improve performance (RNF1.1, RNF1.2)

import json
import redis
from typing import Optional, Any
from config import settings


class CacheService:
    """Service for Redis caching operations"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.ttl = settings.cache_ttl
        self._connect()
    
    def _connect(self):
        """Establish Redis connection"""
        try:
            self.redis_client = redis.from_url(
                settings.redis_url,
                decode_responses=True,
                socket_connect_timeout=5
            )
            # Test connection
            self.redis_client.ping()
            print(f"✓ Redis connected successfully at {settings.redis_url}")
        except Exception as e:
            print(f"⚠ Warning: Redis connection failed: {e}")
            print("  Cache will be disabled. Service will continue without caching.")
            self.redis_client = None
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or cache unavailable
        """
        if not self.redis_client:
            return None
        
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set value in cache
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (default: settings.cache_ttl)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.redis_client:
            return False
        
        try:
            ttl = ttl or self.ttl
            serialized_value = json.dumps(value)
            self.redis_client.setex(key, ttl, serialized_value)
            return True
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Delete value from cache
        
        Args:
            key: Cache key
            
        Returns:
            True if successful, False otherwise
        """
        if not self.redis_client:
            return False
        
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False
    
    def delete_pattern(self, pattern: str) -> bool:
        """
        Delete all keys matching pattern
        
        Args:
            pattern: Pattern to match (e.g., "books:*")
            
        Returns:
            True if successful, False otherwise
        """
        if not self.redis_client:
            return False
        
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
            return True
        except Exception as e:
            print(f"Cache delete pattern error: {e}")
            return False
    
    def clear_all(self) -> bool:
        """
        Clear all cache
        
        Returns:
            True if successful, False otherwise
        """
        if not self.redis_client:
            return False
        
        try:
            self.redis_client.flushdb()
            return True
        except Exception as e:
            print(f"Cache clear error: {e}")
            return False
    
    def is_available(self) -> bool:
        """
        Check if cache is available
        
        Returns:
            True if Redis is connected, False otherwise
        """
        return self.redis_client is not None


# Global cache service instance
cache_service = CacheService()
