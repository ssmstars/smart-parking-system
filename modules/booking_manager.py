"""
Booking Management Module
Handles all booking operations for users
"""

from database.db_manager import DatabaseManager
from utils.helpers import Helper
from utils.validators import Validator
from datetime import datetime, timedelta


class BookingManager:
    """Manages parking booking operations"""
    
    # Booking packages with rates
    PACKAGES = {
        'hourly': {'name': 'Hourly', 'rate': 50, 'duration_hours': 1},
        'half_day': {'name': 'Half Day (6 hours)', 'rate': 250, 'duration_hours': 6},
        'full_day': {'name': 'Full Day (24 hours)', 'rate': 400, 'duration_hours': 24},
        'weekly': {'name': 'Weekly (7 days)', 'rate': 2500, 'duration_hours': 168},
        'monthly': {'name': 'Monthly (30 days)', 'rate': 8000, 'duration_hours': 720}
    }
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def book_slot(self, user_id, slot_id, vehicle_number, booking_date=None, booking_time=None, package='hourly'):
        """Book a parking slot with date, time and package"""
        # Validate vehicle number
        if not Validator.validate_vehicle_number(vehicle_number):
            return {'success': False, 'message': 'Invalid vehicle number format.'}
        
        vehicle_number = vehicle_number.upper()
        
        # Check if slot is available
        slot_query = "SELECT status, slot_number FROM slots WHERE id = ?"
        slot = self.db.fetch_one(slot_query, (slot_id,))
        
        if not slot:
            return {'success': False, 'message': 'Slot not found.'}
        
        if slot[0] != 'Available':
            return {'success': False, 'message': 'Slot is not available.'}
        
        # Check if user has active bookings
        active_query = "SELECT COUNT(*) FROM bookings WHERE user_id = ? AND status = 'Active'"
        active_count = self.db.fetch_one(active_query, (user_id,))[0]
        
        if active_count > 0:
            return {'success': False, 'message': 'You already have an active booking. Please cancel it first.'}
        
        # Parse booking datetime
        if booking_date and booking_time:
            try:
                booking_datetime = datetime.strptime(f"{booking_date} {booking_time}", "%Y-%m-%d %H:%M")
                
                # Validate booking time is not in the past
                current_time = datetime.now()
                if booking_datetime < current_time:
                    return {'success': False, 'message': 'Booking time cannot be in the past.'}
                
                booking_time_str = booking_datetime.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                return {'success': False, 'message': 'Invalid date or time format.'}
        else:
            # Use current time if not specified
            booking_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Get package details
        package_info = self.PACKAGES.get(package, self.PACKAGES['hourly'])
        
        # Create booking with package info
        insert_query = """
            INSERT INTO bookings (user_id, slot_id, vehicle_number, booking_time, status, package_type, package_cost, expected_duration)
            VALUES (?, ?, ?, ?, 'Active', ?, ?, ?)
        """
        success = self.db.execute_query(insert_query, (
            user_id, slot_id, vehicle_number, booking_time_str, 
            package_info['name'], package_info['rate'], package_info['duration_hours']
        ))
        
        if success:
            # Update slot status to Occupied
            update_query = "UPDATE slots SET status = 'Occupied' WHERE id = ?"
            self.db.execute_query(update_query, (slot_id,))
            
            return {
                'success': True,
                'message': f'Slot {slot[1]} booked successfully!',
                'slot_number': slot[1],
                'package': package_info['name'],
                'cost': package_info['rate']
            }
        
        return {'success': False, 'message': 'Booking failed. Please try again.'}
    
    def cancel_booking(self, booking_id, user_id):
        """Cancel an active booking with actual cost calculation"""
        # Get booking details
        booking_query = """
            SELECT b.id, b.slot_id, b.user_id, s.slot_number, b.booking_time, b.package_type, b.package_cost, b.expected_duration
            FROM bookings b
            JOIN slots s ON b.slot_id = s.id
            WHERE b.id = ? AND b.user_id = ? AND b.status = 'Active'
        """
        booking = self.db.fetch_one(booking_query, (booking_id, user_id))
        
        if not booking:
            return {'success': False, 'message': 'Booking not found or already cancelled.'}
        
        slot_id = booking[1]
        slot_number = booking[3]
        booking_time = booking[4]
        package_type = booking[5]
        package_cost = booking[6] if booking[6] else 50.0
        expected_duration = booking[7] if booking[7] else 1.0
        
        # Calculate duration and cost using system time
        checkout_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        duration = Helper.calculate_duration(booking_time, checkout_time)
        
        # Calculate actual cost (either package cost or hourly rate, whichever is higher for fairness)
        hourly_cost = Helper.calculate_cost(duration)
        actual_cost = max(package_cost, hourly_cost) if duration > expected_duration else package_cost
        
        # Round to 2 decimal places
        actual_cost = round(actual_cost, 2)
        duration = round(duration, 2)
        
        # Update booking status with actual cost
        update_booking = """
            UPDATE bookings 
            SET status = 'Completed', checkout_time = ?, actual_cost = ?
            WHERE id = ?
        """
        success = self.db.execute_query(update_booking, (checkout_time, actual_cost, booking_id))
        
        if success:
            # Update slot status to Available
            update_slot = "UPDATE slots SET status = 'Available' WHERE id = ?"
            self.db.execute_query(update_slot, (slot_id,))
            
            return {
                'success': True,
                'message': f'Checkout successful!',
                'slot_number': slot_number,
                'duration': duration,
                'package': package_type,
                'package_cost': package_cost,
                'actual_cost': actual_cost,
                'checkout_time': datetime.now().strftime("%d-%b-%Y %I:%M %p")
            }
        
        return {'success': False, 'message': 'Failed to cancel booking.'}
    
    def get_user_bookings(self, user_id, status=None):
        """Get all bookings for a user"""
        if status:
            query = """
                SELECT b.id, s.slot_number, s.slot_type, b.vehicle_number, 
                       b.booking_time, b.checkout_time, b.status, b.package_type, b.package_cost, b.actual_cost
                FROM bookings b
                JOIN slots s ON b.slot_id = s.id
                WHERE b.user_id = ? AND b.status = ?
                ORDER BY b.booking_time DESC
            """
            return self.db.fetch_all(query, (user_id, status))
        else:
            query = """
                SELECT b.id, s.slot_number, s.slot_type, b.vehicle_number, 
                       b.booking_time, b.checkout_time, b.status, b.package_type, b.package_cost, b.actual_cost
                FROM bookings b
                JOIN slots s ON b.slot_id = s.id
                WHERE b.user_id = ?
                ORDER BY b.booking_time DESC
            """
            return self.db.fetch_all(query, (user_id,))
    
    def get_active_booking(self, user_id):
        """Get active booking for a user"""
        query = """
            SELECT b.id, s.slot_number, s.slot_type, b.vehicle_number, 
                   b.booking_time, s.floor, b.package_type, b.package_cost, b.expected_duration
            FROM bookings b
            JOIN slots s ON b.slot_id = s.id
            WHERE b.user_id = ? AND b.status = 'Active'
        """
        return self.db.fetch_one(query, (user_id,))
    
    def get_all_bookings(self):
        """Get all bookings (Admin view)"""
        query = """
            SELECT b.id, u.username, s.slot_number, b.vehicle_number, 
                   b.booking_time, b.checkout_time, b.status
            FROM bookings b
            JOIN users u ON b.user_id = u.id
            JOIN slots s ON b.slot_id = s.id
            ORDER BY b.booking_time DESC
        """
        return self.db.fetch_all(query)
    
    def get_active_bookings(self):
        """Get all active bookings (Admin view)"""
        query = """
            SELECT b.id, u.username, u.phone, s.slot_number, b.vehicle_number, 
                   b.booking_time
            FROM bookings b
            JOIN users u ON b.user_id = u.id
            JOIN slots s ON b.slot_id = s.id
            WHERE b.status = 'Active'
            ORDER BY b.booking_time DESC
        """
        return self.db.fetch_all(query)
    
    def get_booking_statistics(self):
        """Get booking statistics (Admin)"""
        total_query = "SELECT COUNT(*) FROM bookings"
        active_query = "SELECT COUNT(*) FROM bookings WHERE status = 'Active'"
        completed_query = "SELECT COUNT(*) FROM bookings WHERE status = 'Completed'"
        
        total = self.db.fetch_one(total_query)[0]
        active = self.db.fetch_one(active_query)[0]
        completed = self.db.fetch_one(completed_query)[0]
        
        return {
            'total': total,
            'active': active,
            'completed': completed
        }
