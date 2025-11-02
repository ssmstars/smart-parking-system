"""
Quick test to verify the enhanced active bookings display
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from modules.booking_manager import BookingManager
from modules.slot_manager import SlotManager
from utils.helpers import Helper

print("=" * 80)
print("TESTING ENHANCED ACTIVE BOOKINGS")
print("=" * 80)

booking_mgr = BookingManager()

# Check for active bookings
print("\n1. Checking active bookings...")
from database.db_manager import DatabaseManager
db = DatabaseManager()

active_bookings_query = """
    SELECT b.id, u.username, s.slot_number, b.vehicle_number, b.booking_time
    FROM bookings b
    JOIN users u ON b.user_id = u.id
    JOIN slots s ON b.slot_id = s.id
    WHERE b.status = 'Active'
"""
active = db.fetch_all(active_bookings_query)

if active:
    print(f"   Found {len(active)} active booking(s):")
    for booking in active:
        print(f"\n   Booking ID: {booking[0]}")
        print(f"   User: {booking[1]}")
        print(f"   Slot: {booking[2]}")
        print(f"   Vehicle: {booking[3]}")
        print(f"   Booking Time: {booking[4]}")
        
        # Test new helper function
        duration_info = Helper.calculate_duration_detailed(booking[4])
        print(f"   Duration (decimal): {duration_info['hours']} hours")
        print(f"   Duration (detailed): {duration_info['display']}")
        print(f"   Total seconds: {duration_info['total_seconds']}s")
else:
    print("   No active bookings found.")
    print("\n   Creating a test booking for demonstration...")
    
    # Create a test booking
    slot_mgr = SlotManager()
    available = slot_mgr.get_available_slots()
    
    if available:
        result = booking_mgr.book_slot(1, available[0][0], 'DEMO1234', package='hourly')
        print(f"   Result: {result}")
        
        if result['success']:
            print("\n   ✅ Test booking created!")
            print("   You can now test the dashboard at: http://localhost:5000")
            print("   Login as: user1 / user123")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
print("\nNext steps:")
print("1. Start the Flask app: python app.py")
print("2. Login as user1")
print("3. Watch the duration timer update in real-time!")
print("=" * 80)
