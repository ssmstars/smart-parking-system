"""
Real-time check of database bookings
"""
import sqlite3
from datetime import datetime

conn = sqlite3.connect('smart_parking.db')
cursor = conn.cursor()

print("=" * 80)
print("CURRENT DATABASE STATUS - " + datetime.now().strftime("%H:%M:%S"))
print("=" * 80)

# Check all bookings
print("\nALL BOOKINGS:")
cursor.execute("""
    SELECT b.id, u.username, s.slot_number, b.vehicle_number, 
           b.booking_time, b.checkout_time, b.status
    FROM bookings b
    JOIN users u ON b.user_id = u.id
    JOIN slots s ON b.slot_id = s.id
    ORDER BY b.id DESC
    LIMIT 10
""")
bookings = cursor.fetchall()

for b in bookings:
    status_icon = "✅" if b[6] == "Active" else "✓"
    print(f"\n{status_icon} ID: {b[0]} | User: {b[1]} | Slot: {b[2]} | Vehicle: {b[3]}")
    print(f"  Booked: {b[4]} | Checkout: {b[5]} | Status: {b[6]}")

# Check active bookings
print("\n" + "=" * 80)
print("ACTIVE BOOKINGS:")
cursor.execute("""
    SELECT b.id, u.username, s.slot_number, b.vehicle_number, b.booking_time
    FROM bookings b
    JOIN users u ON b.user_id = u.id
    JOIN slots s ON b.slot_id = s.id
    WHERE b.status = 'Active'
""")
active = cursor.fetchall()

if active:
    for a in active:
        print(f"\n✅ ID: {a[0]} | User: {a[1]} | Slot: {a[2]} | Vehicle: {a[3]}")
        print(f"   Since: {a[4]}")
else:
    print("\n❌ NO ACTIVE BOOKINGS")

# Check slot status
print("\n" + "=" * 80)
print("SLOT STATUS:")
cursor.execute("SELECT status, COUNT(*) FROM slots GROUP BY status")
for status in cursor.fetchall():
    print(f"  {status[0]}: {status[1]}")

conn.close()
print("=" * 80)
