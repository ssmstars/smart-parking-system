"""
Authentication Module
Handles user and admin login/registration
"""

from database.db_manager import DatabaseManager
from utils.validators import Validator


class Authentication:
    """Authentication class for login and registration"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def admin_login(self, username, password):
        """Admin login verification"""
        query = "SELECT id, username, email FROM admin WHERE username = ? AND password = ?"
        result = self.db.fetch_one(query, (username, password))
        
        if result:
            return {
                'success': True,
                'user_id': result[0],
                'username': result[1],
                'email': result[2],
                'role': 'admin'
            }
        return {'success': False, 'message': 'Invalid admin credentials'}
    
    def user_login(self, username, password):
        """User login verification"""
        query = "SELECT id, username, email, phone, vehicle_number FROM users WHERE username = ? AND password = ?"
        result = self.db.fetch_one(query, (username, password))
        
        if result:
            return {
                'success': True,
                'user_id': result[0],
                'username': result[1],
                'email': result[2],
                'phone': result[3],
                'vehicle_number': result[4],
                'role': 'user'
            }
        return {'success': False, 'message': 'Invalid user credentials'}
    
    def register_user(self, username, password, email, phone, vehicle_number):
        """Register new user"""
        # Validate inputs
        if not Validator.validate_username(username):
            return {'success': False, 'message': 'Invalid username. Use 3-20 alphanumeric characters.'}
        
        if not Validator.validate_password(password):
            return {'success': False, 'message': 'Password must be at least 6 characters long.'}
        
        if not Validator.validate_email(email):
            return {'success': False, 'message': 'Invalid email format.'}
        
        if not Validator.validate_phone(phone):
            return {'success': False, 'message': 'Invalid phone number. Use 10 digits.'}
        
        if not Validator.validate_vehicle_number(vehicle_number):
            return {'success': False, 'message': 'Invalid vehicle number format.'}
        
        # Check if username already exists
        check_query = "SELECT id FROM users WHERE username = ? OR email = ?"
        existing = self.db.fetch_one(check_query, (username, email))
        
        if existing:
            return {'success': False, 'message': 'Username or email already exists.'}
        
        # Insert new user
        insert_query = """
            INSERT INTO users (username, password, email, phone, vehicle_number)
            VALUES (?, ?, ?, ?, ?)
        """
        success = self.db.execute_query(
            insert_query,
            (username, password, email, phone, vehicle_number.upper())
        )
        
        if success:
            return {'success': True, 'message': 'Registration successful! You can now login.'}
        return {'success': False, 'message': 'Registration failed. Please try again.'}
    
    def add_admin(self, username, password, email):
        """Add new admin account (admin only)"""
        if not Validator.validate_username(username):
            return {'success': False, 'message': 'Invalid username.'}
        
        if not Validator.validate_password(password):
            return {'success': False, 'message': 'Password must be at least 6 characters long.'}
        
        if email and not Validator.validate_email(email):
            return {'success': False, 'message': 'Invalid email format.'}
        
        # Check if username already exists
        check_query = "SELECT id FROM admin WHERE username = ?"
        existing = self.db.fetch_one(check_query, (username,))
        
        if existing:
            return {'success': False, 'message': 'Admin username already exists.'}
        
        # Insert new admin
        insert_query = "INSERT INTO admin (username, password, email) VALUES (?, ?, ?)"
        success = self.db.execute_query(insert_query, (username, password, email))
        
        if success:
            return {'success': True, 'message': 'Admin account created successfully.'}
        return {'success': False, 'message': 'Failed to create admin account.'}
