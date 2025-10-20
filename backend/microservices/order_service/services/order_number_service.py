# Order Number Service - Generates unique order numbers
# Implements sequential order number generation

import random
import string
from datetime import datetime
from typing import Optional

from config import settings


class OrderNumberService:
    """Service for generating unique order numbers"""
    
    def generate_order_number(self, last_order_number: Optional[str] = None) -> str:
        """
        Generate a unique order number
        
        Format: MP-YYYYMMDD-NNNN
        Example: MP-20241016-0001
        
        Args:
            last_order_number: Last order number for sequential generation
            
        Returns:
            Generated order number
        """
        prefix = settings.order_number_prefix
        date_str = datetime.now().strftime("%Y%m%d")
        
        # Extract sequential number from last order
        sequential = 1
        if last_order_number:
            try:
                # Extract the last 4 digits
                parts = last_order_number.split('-')
                if len(parts) == 3 and parts[1] == date_str:
                    sequential = int(parts[2]) + 1
            except (ValueError, IndexError):
                pass
        
        # Format: MP-YYYYMMDD-NNNN
        order_number = f"{prefix}-{date_str}-{sequential:04d}"
        
        return order_number
    
    def validate_order_number(self, order_number: str) -> bool:
        """
        Validate order number format
        
        Args:
            order_number: Order number to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            parts = order_number.split('-')
            if len(parts) != 3:
                return False
            
            prefix, date_str, sequential = parts
            
            # Validate prefix
            if prefix != settings.order_number_prefix:
                return False
            
            # Validate date format
            datetime.strptime(date_str, "%Y%m%d")
            
            # Validate sequential number
            int(sequential)
            
            return True
        except (ValueError, AttributeError):
            return False


# Global instance
order_number_service = OrderNumberService()
