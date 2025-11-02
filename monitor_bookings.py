"""
Monitor for new bookings
"""
import sqlite3
import time

conn = sqlite3.connect('smart_parking.db')
cursor = conn.cursor()

print("Monitoring for new bookings... (checking every 2 seconds)")
print("Press Ctrl+C to stop")
print("=" * 80)

last_count = 0
cursor.execute("SELECT COUNT(*) FROM bookings")
last_count = cursor.fetchone()[0]

try:
    while True:
        cursor.execute("SELECT COUNT(*) FROM bookings")
        current_count = cursor.fetchone()[0]
        
        if current_count > last_count:
            print(f"\n🆕 NEW BOOKING DETECTED! (Total: {current_count})")
            
            # Get the latest booking
            cursor.execute("""
                SELECT b.id, u.username, s.slot_number, b.vehicle_number, 
                       b.status, b.booking_time
                FROM bookings b
                JOIN users u ON b.user_id = u.id
                JOIN slots s ON b.slot_id = s.id
                ORDER BY b.id DESC
                LIMIT 1
            """)
            booking = cursor.fetchone()
            
            print(f"   ID: {booking[0]}")
            print(f"   User: {booking[1]}")
            print(f"   Slot: {booking[2]}")
            print(f"   Vehicle: {booking[3]}")
            print(f"   Status: {booking[4]}")
            print(f"   Time: {booking[5]}")
            print("=" * 80)
            
            last_count = current_count
        
        time.sleep(2)
        
except KeyboardInterrupt:
    print("\n\nMonitoring stopped.")
    conn.close()
