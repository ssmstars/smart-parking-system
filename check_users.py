"""
Check which users have active bookings
"""
import sqlite3

conn = sqlite3.connect('smart_parking.db')
cursor = conn.cursor()

print("=" * 80)
print("USER AND BOOKING STATUS CHECK")
print("=" * 80)

# Get all users
print("\n1. All Users:")
cursor.execute("SELECT id, username, email FROM users")
users = cursor.fetchall()

for user in users:
    print(f"\n   User ID: {user[0]}")
    print(f"   Username: {user[1]}")
    print(f"   Email: {user[2]}")
    
    # Check for active bookings
    cursor.execute("""
        SELECT b.id, s.slot_number, b.vehicle_number, b.booking_time
        FROM bookings b
        JOIN slots s ON b.slot_id = s.id
        WHERE b.user_id = ? AND b.status = 'Active'
    """, (user[0],))
    
    active = cursor.fetchone()
    
    if active:
        print(f"   ✅ HAS ACTIVE BOOKING:")
        print(f"      Booking ID: {active[0]}")
        print(f"      Slot: {active[1]}")
        print(f"      Vehicle: {active[2]}")
        print(f"      Since: {active[3]}")
    else:
        print(f"   ❌ No active booking")

print("\n" + "=" * 80)
print("RECOMMENDATION")
print("=" * 80)

cursor.execute("""
    SELECT u.username, b.id, s.slot_number, b.vehicle_number
    FROM bookings b
    JOIN users u ON b.user_id = u.id
    JOIN slots s ON b.slot_id = s.id
    WHERE b.status = 'Active'
""")

active_bookings = cursor.fetchall()

if active_bookings:
    print("\nTo see active parking, login as:")
    for booking in active_bookings:
        print(f"   Username: {booking[0]}")
        print(f"   Password: user123")  # Default password
        print(f"   (They have booking #{booking[1]} on slot {booking[2]})")
else:
    print("\nNo active bookings found. You can:")
    print("   1. Login as any user")
    print("   2. Book a new parking slot")
    print("   3. See it appear in your dashboard!")

conn.close()

print("\n" + "=" * 80)
