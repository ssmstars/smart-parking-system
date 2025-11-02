"""
Helper utilities for common operations
"""

from datetime import datetime


class Helper:
    """Helper functions for the application"""
    
    @staticmethod
    def format_datetime(dt_string):
        """Format datetime string for display"""
        if not dt_string:
            return "N/A"
        try:
            dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
            return dt.strftime("%d-%b-%Y %I:%M %p")
        except:
            return dt_string
    
    @staticmethod
    def calculate_duration(start_time, end_time=None):
        """Calculate parking duration"""
        if not end_time:
            end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            start = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            end = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
            duration = end - start
            
            hours = duration.total_seconds() / 3600
            return round(hours, 2)
        except:
            return 0
    
    @staticmethod
    def calculate_cost(hours, rate_per_hour=50):
        """Calculate parking cost based on hours"""
        if hours < 1:
            return rate_per_hour  # Minimum charge
        return round(hours * rate_per_hour, 2)
    
    @staticmethod
    def get_current_timestamp():
        """Get current timestamp"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
