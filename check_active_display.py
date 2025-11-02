"""
Check for any issues with active bookings display
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from modules.booking_manager import BookingManager
from utils.helpers import Helper
from datetime import datetime, timedelta

print("=" * 80)
print("ACTIVE BOOKINGS DISPLAY CHECK")
print("=" * 80)

booking_mgr = BookingManager()

# Get current active bookings
print("\n1. Checking for active bookings...")
from database.db_manager import DatabaseManager
db = DatabaseManager()

# Check all users
users_query = "SELECT id, username FROM users"
users = db.fetch_all(users_query)

print(f"\n   Found {len(users)} users")

for user in users:
    user_id = user[0]
    username = user[1]
    active = booking_mgr.get_active_booking(user_id)
    
    if active:
        print(f"\n   ✅ User '{username}' (ID: {user_id}) has active booking:")
        print(f"      Booking ID: {active[0]}")
        print(f"      Slot: {active[1]}")
        print(f"      Vehicle: {active[3]}")
        print(f"      Booking Time: {active[4]}")
        
        # Calculate duration
        duration = Helper.calculate_duration(active[4])
        cost = Helper.calculate_cost(duration)
        
        print(f"      Duration: {duration} hours")
        print(f"      Cost: ₹{cost}")
        
        # Check if duration is suspiciously low
        booking_time = datetime.strptime(active[4], "%Y-%m-%d %H:%M:%S")
        now = datetime.now()
        time_diff = now - booking_time
        minutes = time_diff.total_seconds() / 60
        
        print(f"      Time since booking: {minutes:.2f} minutes")
        
        if duration == 0.0 and minutes > 1:
            print(f"      ⚠️ WARNING: Duration shows 0.0 but {minutes:.2f} minutes have passed!")
    else:
        print(f"   - User '{username}' (ID: {user_id}): No active booking")

# Check admin view
print("\n2. Checking admin active bookings view...")
admin_active = booking_mgr.get_active_bookings()
print(f"   Admin view shows {len(admin_active)} active booking(s)")

if admin_active:
    for booking in admin_active:
        print(f"\n   Booking ID: {booking[0]}")
        print(f"   User: {booking[1]} (Phone: {booking[2]})")
        print(f"   Slot: {booking[3]}")
        print(f"   Vehicle: {booking[4]}")
        print(f"   Booking Time: {booking[5]}")

# Check statistics
print("\n3. Booking statistics:")
stats = booking_mgr.get_booking_statistics()
print(f"   Total: {stats['total']}")
print(f"   Active: {stats['active']}")
print(f"   Completed: {stats['completed']}")

if stats['active'] == 0:
    print("\n   ⚠️ NO ACTIVE BOOKINGS FOUND!")
    print("   This might be the issue the user is experiencing.")
    print("\n   Solutions:")
    print("   1. Make sure users are booking slots through the web interface")
    print("   2. Check if bookings are being auto-completed somehow")
    print("   3. Verify the booking status is being set correctly")
elif stats['active'] > 0:
    print("\n   ✅ Active bookings are present and should display correctly!")

print("\n" + "=" * 80)
print("CHECK COMPLETE")
print("=" * 80)
