"""
Test script to verify booking flow and active bookings display
"""
import sqlite3
from datetime import datetime

# Connect to database
conn = sqlite3.connect('smart_parking.db')
cursor = conn.cursor()

print("=" * 80)
print("TESTING ACTIVE BOOKINGS FLOW")
print("=" * 80)

# Create a test active booking
print("\n1. Creating a test active booking...")
test_user_id = 1
test_slot_id = 1

# First check if slot is available
cursor.execute("SELECT status FROM slots WHERE id = ?", (test_slot_id,))
slot_status = cursor.fetchone()
print(f"   Slot {test_slot_id} status: {slot_status[0]}")

if slot_status[0] == 'Available':
    # Create an active booking
    booking_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO bookings (user_id, slot_id, vehicle_number, booking_time, status, package_type, package_cost, expected_duration)
        VALUES (?, ?, ?, ?, 'Active', 'Hourly', 50, 1)
    """, (test_user_id, test_slot_id, 'TEST1234', booking_time))
    
    # Update slot status
    cursor.execute("UPDATE slots SET status = 'Occupied' WHERE id = ?", (test_slot_id,))
    conn.commit()
    print("   ✅ Test booking created successfully!")
else:
    print(f"   ⚠️ Slot {test_slot_id} is already {slot_status[0]}")

# Now test the active booking query
print("\n2. Testing get_active_booking query:")
query = """
    SELECT b.id, s.slot_number, s.slot_type, b.vehicle_number, 
           b.booking_time, s.floor, b.package_type, b.package_cost, b.expected_duration
    FROM bookings b
    JOIN slots s ON b.slot_id = s.id
    WHERE b.user_id = ? AND b.status = 'Active'
"""
cursor.execute(query, (test_user_id,))
result = cursor.fetchone()

if result:
    print(f"   ✅ Active booking found!")
    print(f"   Booking ID: {result[0]}")
    print(f"   Slot Number: {result[1]}")
    print(f"   Slot Type: {result[2]}")
    print(f"   Vehicle: {result[3]}")
    print(f"   Booking Time: {result[4]}")
    print(f"   Floor: {result[5]}")
    print(f"   Package: {result[6]}")
    print(f"   Cost: ₹{result[7]}")
    print(f"   Expected Duration: {result[8]} hours")
else:
    print("   ❌ No active booking found!")

# Test admin view
print("\n3. Testing admin active bookings view:")
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

if admin_active:
    print(f"   ✅ Found {len(admin_active)} active booking(s)")
    for booking in admin_active:
        print(f"   - Booking ID: {booking[0]}")
        print(f"     User: {booking[1]}")
        print(f"     Phone: {booking[2]}")
        print(f"     Slot: {booking[3]}")
        print(f"     Vehicle: {booking[4]}")
        print(f"     Time: {booking[5]}")
else:
    print("   ❌ No active bookings in admin view!")

# Check slot status
print("\n4. Checking slot statuses:")
cursor.execute("SELECT status, COUNT(*) FROM slots GROUP BY status")
statuses = cursor.fetchall()
for status in statuses:
    print(f"   {status[0]}: {status[1]} slots")

print("\n" + "=" * 80)
print("Would you like to:")
print("1. Keep this test booking active (to see dashboard)")
print("2. Clean up the test booking")
print("=" * 80)

response = input("\nEnter choice (1 or 2): ").strip()

if response == "2":
    print("\n5. Cleaning up test booking...")
    cursor.execute("DELETE FROM bookings WHERE vehicle_number = 'TEST1234'")
    cursor.execute("UPDATE slots SET status = 'Available' WHERE id = ?", (test_slot_id,))
    conn.commit()
    print("   ✅ Test booking removed!")
else:
    print("\n   ℹ️ Test booking kept active. You can now view it in the dashboard!")
    print("   Login with: user1 / user123")

conn.close()
print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
