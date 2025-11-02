"""
Database Manager Module
Handles all database operations for the Smart Parking System
"""

import sqlite3
from datetime import datetime
import os


class DatabaseManager:
    """Manages all database operations for the parking system"""
    
    def __init__(self, db_name="smart_parking.db"):
        """Initialize database connection"""
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), db_name)
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
        self.create_default_admin()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
            return True
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            return False
    
    def create_tables(self):
        """Create all necessary tables if they don't exist"""
        try:
            # Admin table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS admin (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Users table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    vehicle_number TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Parking slots table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS slots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    slot_number TEXT UNIQUE NOT NULL,
                    slot_type TEXT DEFAULT 'Regular',
                    status TEXT DEFAULT 'Available',
                    floor INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Bookings table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    slot_id INTEGER NOT NULL,
                    vehicle_number TEXT NOT NULL,
                    booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    checkout_time TIMESTAMP,
                    status TEXT DEFAULT 'Active',
                    package_type TEXT DEFAULT 'Hourly',
                    package_cost REAL DEFAULT 50,
                    expected_duration REAL DEFAULT 1,
                    actual_cost REAL,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (slot_id) REFERENCES slots(id)
                )
            ''')
            
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
            return False
    
    def create_default_admin(self):
        """Create default admin account if none exists"""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM admin")
            count = self.cursor.fetchone()[0]
            
            if count == 0:
                self.cursor.execute(
                    "INSERT INTO admin (username, password, email) VALUES (?, ?, ?)",
                    ("admin", "admin123", "admin@smartparking.com")
                )
                self.conn.commit()
                print("Default admin created: username='admin', password='admin123'")
        except sqlite3.Error as e:
            print(f"Error creating default admin: {e}")
    
    def execute_query(self, query, params=()):
        """Execute a query and return results"""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Query execution error: {e}")
            return False
    
    def fetch_one(self, query, params=()):
        """Fetch single record"""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Fetch error: {e}")
            return None
    
    def fetch_all(self, query, params=()):
        """Fetch all records"""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Fetch error: {e}")
            return []
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        """Destructor to ensure connection is closed"""
        self.close()
