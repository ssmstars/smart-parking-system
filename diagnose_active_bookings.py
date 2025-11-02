"""
Comprehensive diagnosis of active bookings issue
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from modules.booking_manager import BookingManager
from modules.slot_manager import SlotManager
from utils.helpers import Helper
from datetime import datetime

print("=" * 80)
print("ACTIVE BOOKINGS DIAGNOSIS")
print("=" * 80)

booking_mgr = BookingManager()
slot_mgr = SlotManager()

# Test 1: Create an active booking programmatically
print("\n1. Testing booking creation...")
test_user_id = 1

# Check for existing active bookings
existing = booking_mgr.get_active_booking(test_user_id)
if existing:
    print(f"   ⚠️ User already has active booking: {existing}")
    print(f"   Canceling it first...")
    booking_mgr.cancel_booking(existing[0], test_user_id)

# Get an available slot
available_slots = slot_mgr.get_available_slots()
if not available_slots:
    print("   ❌ No available slots!")
    sys.exit(1)

test_slot_id = available_slots[0][0]
print(f"   Using slot ID: {test_slot_id}, Number: {available_slots[0][1]}")

# Book the slot
result = booking_mgr.book_slot(test_user_id, test_slot_id, 'TEST9999')
print(f"   Booking result: {result}")

if not result['success']:
    print(f"   ❌ Booking failed: {result['message']}")
    sys.exit(1)

# Test 2: Retrieve active booking
print("\n2. Testing get_active_booking...")
active_booking = booking_mgr.get_active_booking(test_user_id)

if active_booking:
    print(f"   ✅ Active booking found!")
    print(f"   Data structure: {active_booking}")
    print(f"   Fields:")
    print(f"     [0] ID: {active_booking[0]}")
    print(f"     [1] Slot Number: {active_booking[1]}")
    print(f"     [2] Slot Type: {active_booking[2]}")
    print(f"     [3] Vehicle: {active_booking[3]}")
    print(f"     [4] Booking Time: {active_booking[4]}")
    print(f"     [5] Floor: {active_booking[5]}")
    print(f"     [6] Package Type: {active_booking[6] if len(active_booking) > 6 else 'N/A'}")
    print(f"     [7] Package Cost: {active_booking[7] if len(active_booking) > 7 else 'N/A'}")
    print(f"     [8] Expected Duration: {active_booking[8] if len(active_booking) > 8 else 'N/A'}")
else:
    print("   ❌ No active booking found!")
    sys.exit(1)

# Test 3: Calculate duration and cost (simulating user_dashboard)
print("\n3. Testing duration and cost calculation...")
try:
    duration = Helper.calculate_duration(active_booking[4])
    cost = Helper.calculate_cost(duration)
    print(f"   ✅ Duration calculated: {duration} hours")
    print(f"   ✅ Cost calculated: ₹{cost}")
    
    # Build booking_info like in app.py
    booking_info = {
        'id': active_booking[0],
        'slot_number': active_booking[1],
        'slot_type': active_booking[2],
        'vehicle_number': active_booking[3],
        'booking_time': Helper.format_datetime(active_booking[4]),
        'floor': active_booking[5],
        'duration': duration,
        'cost': cost
    }
    print(f"\n   Booking Info Dictionary:")
    for key, value in booking_info.items():
        print(f"     {key}: {value}")
except Exception as e:
    print(f"   ❌ Error calculating duration/cost: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Test admin view
print("\n4. Testing admin active bookings view...")
admin_active = booking_mgr.get_active_bookings()
print(f"   Found {len(admin_active)} active booking(s)")
if admin_active:
    for booking in admin_active:
        print(f"   - ID: {booking[0]}, User: {booking[1]}, Slot: {booking[3]}, Vehicle: {booking[4]}")

# Test 5: Get booking statistics
print("\n5. Testing booking statistics...")
stats = booking_mgr.get_booking_statistics()
print(f"   Total: {stats['total']}")
print(f"   Active: {stats['active']}")
print(f"   Completed: {stats['completed']}")

# Test 6: Wait a few seconds and recalculate
print("\n6. Testing duration updates...")
import time
print("   Waiting 5 seconds...")
time.sleep(5)

active_booking_2 = booking_mgr.get_active_booking(test_user_id)
if active_booking_2:
    duration_2 = Helper.calculate_duration(active_booking_2[4])
    cost_2 = Helper.calculate_cost(duration_2)
    print(f"   ✅ Updated duration: {duration_2} hours (was {duration})")
    print(f"   ✅ Updated cost: ₹{cost_2} (was ₹{cost})")

# Cleanup
print("\n7. Cleanup...")
response = input("\nDelete test booking? (y/n): ").strip().lower()
if response == 'y':
    cancel_result = booking_mgr.cancel_booking(active_booking[0], test_user_id)
    print(f"   Cancel result: {cancel_result}")
else:
    print("   Test booking kept. Login as user1 to see it in dashboard.")

print("\n" + "=" * 80)
print("DIAGNOSIS COMPLETE")
print("=" * 80)
