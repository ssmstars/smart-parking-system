"""
Validation utilities for input validation
"""

import re


class Validator:
    """Input validation class"""
    
    @staticmethod
    def validate_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_phone(phone):
        """Validate phone number (10 digits)"""
        pattern = r'^[0-9]{10}$'
        return re.match(pattern, phone) is not None
    
    @staticmethod
    def validate_vehicle_number(vehicle_number):
        """Validate vehicle number format"""
        # Simple validation - can be customized based on region
        pattern = r'^[A-Z0-9-]{4,15}$'
        return re.match(pattern, vehicle_number.upper()) is not None
    
    @staticmethod
    def validate_username(username):
        """Validate username (alphanumeric, 3-20 chars)"""
        if len(username) < 3 or len(username) > 20:
            return False
        pattern = r'^[a-zA-Z0-9_]+$'
        return re.match(pattern, username) is not None
    
    @staticmethod
    def validate_password(password):
        """Validate password (minimum 6 characters)"""
        return len(password) >= 6
    
    @staticmethod
    def validate_slot_number(slot_number):
        """Validate slot number format"""
        pattern = r'^[A-Z0-9-]{1,10}$'
        return re.match(pattern, slot_number.upper()) is not None
