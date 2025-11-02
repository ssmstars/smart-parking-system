"""
Test script to check active bookings functionality
"""
import sqlite3
from datetime import datetime

# Connect to database
conn = sqlite3.connect('smart_parking.db')
cursor = conn.cursor()

print("=" * 80)
print("ACTIVE BOOKINGS DIAGNOSTIC TEST")
print("=" * 80)

# Check bookings table structure
print("\n1. Bookings Table Structure:")
cursor.execute("PRAGMA table_info(bookings)")
columns = cursor.fetchall()
for col in columns:
    print(f"   - {col[1]} ({col[2]})")

# Check all bookings
print("\n2. All Bookings:")
cursor.execute("SELECT * FROM bookings")
all_bookings = cursor.fetchall()
print(f"   Total bookings: {len(all_bookings)}")

# Check active bookings (status = 'Active')
print("\n3. Active Bookings (status = 'Active'):")
cursor.execute("SELECT * FROM bookings WHERE status = 'Active'")
active_bookings = cursor.fetchall()
print(f"   Active bookings count: {len(active_bookings)}")
for booking in active_bookings:
    print(f"   - ID: {booking[0]}, User: {booking[1]}, Slot: {booking[2]}, Status: {booking[6]}")

# Test the query used in get_active_booking
print("\n4. Testing get_active_booking query:")
test_user_id = 1
query = """
    SELECT b.id, s.slot_number, s.slot_type, b.vehicle_number, 
           b.booking_time, s.floor, b.package_type, b.package_cost, b.expected_duration
    FROM bookings b
    JOIN slots s ON b.slot_id = s.id
    WHERE b.user_id = ? AND b.status = 'Active'
"""
cursor.execute(query, (test_user_id,))
result = cursor.fetchone()
print(f"   User {test_user_id} active booking: {result}")

# Check all users with active bookings
print("\n5. All Users with Active Bookings:")
cursor.execute("""
    SELECT DISTINCT u.id, u.username, COUNT(b.id) as active_count
    FROM users u
    JOIN bookings b ON u.id = b.user_id
    WHERE b.status = 'Active'
    GROUP BY u.id, u.username
""")
users_with_active = cursor.fetchall()
for user in users_with_active:
    print(f"   - User ID: {user[0]}, Username: {user[1]}, Active Bookings: {user[2]}")

# Test the admin active bookings query
print("\n6. Admin Active Bookings Query:")
admin_query = """
    SELECT b.id, u.username, u.phone, s.slot_number, b.vehicle_number, 
           b.booking_time
    FROM bookings b
    JOIN users u ON b.user_id = u.id
    JOIN slots s ON b.slot_id = s.id
    WHERE b.status = 'Active'
    ORDER BY b.booking_time DESC
"""
cursor.execute(admin_query)
admin_active = cursor.fetchall()
print(f"   Admin view active bookings: {len(admin_active)}")
for booking in admin_active:
    print(f"   - ID: {booking[0]}, User: {booking[1]}, Slot: {booking[3]}, Vehicle: {booking[4]}")

# Check slots status
print("\n7. Slot Status:")
cursor.execute("SELECT status, COUNT(*) FROM slots GROUP BY status")
slot_status = cursor.fetchall()
for status in slot_status:
    print(f"   - {status[0]}: {status[1]} slots")

# Check if any bookings have null status
print("\n8. Bookings with NULL or empty status:")
cursor.execute("SELECT * FROM bookings WHERE status IS NULL OR status = ''")
null_status = cursor.fetchall()
print(f"   Count: {len(null_status)}")

# Check booking times
print("\n9. Recent Bookings (last 5):")
cursor.execute("""
    SELECT b.id, u.username, s.slot_number, b.booking_time, b.checkout_time, b.status
    FROM bookings b
    JOIN users u ON u.id = b.user_id
    JOIN slots s ON s.id = b.slot_id
    ORDER BY b.booking_time DESC
    LIMIT 5
""")
recent = cursor.fetchall()
for booking in recent:
    print(f"   - ID: {booking[0]}, User: {booking[1]}, Slot: {booking[2]}")
    print(f"     Booking: {booking[3]}, Checkout: {booking[4]}, Status: {booking[5]}")

conn.close()

print("\n" + "=" * 80)
print("DIAGNOSTIC TEST COMPLETE")
print("=" * 80)
