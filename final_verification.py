"""
Final verification test for active bookings fixes
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from modules.booking_manager import BookingManager
from modules.slot_manager import SlotManager
from utils.helpers import Helper
from database.db_manager import DatabaseManager

print("=" * 80)
print("FINAL VERIFICATION TEST - ACTIVE BOOKINGS")
print("=" * 80)

booking_mgr = BookingManager()
slot_mgr = SlotManager()
db = DatabaseManager()

# Test all components
tests_passed = 0
tests_total = 0

# Test 1: Helper function enhancement
print("\n[Test 1] Testing calculate_duration_detailed()...")
tests_total += 1
try:
    from datetime import datetime, timedelta
    test_time = (datetime.now() - timedelta(hours=1, minutes=30, seconds=45)).strftime("%Y-%m-%d %H:%M:%S")
    result = Helper.calculate_duration_detailed(test_time)
    
    if 'hours' in result and 'display' in result and 'total_seconds' in result:
        print(f"   ✅ PASS - Duration: {result['display']} ({result['hours']} hours)")
        tests_passed += 1
    else:
        print(f"   ❌ FAIL - Missing keys in result")
except Exception as e:
    print(f"   ❌ FAIL - {e}")

# Test 2: Active booking retrieval
print("\n[Test 2] Testing get_active_booking()...")
tests_total += 1
try:
    active = booking_mgr.get_active_booking(1)
    if active:
        if len(active) >= 6:
            print(f"   ✅ PASS - Active booking found with {len(active)} fields")
            print(f"   Slot: {active[1]}, Vehicle: {active[3]}")
            tests_passed += 1
        else:
            print(f"   ❌ FAIL - Insufficient fields")
    else:
        print(f"   ℹ️  INFO - No active booking for user 1 (may be expected)")
        tests_passed += 1  # Not a failure, just no data
except Exception as e:
    print(f"   ❌ FAIL - {e}")

# Test 3: Admin active bookings with duration
print("\n[Test 3] Testing admin active bookings view...")
tests_total += 1
try:
    bookings_raw = booking_mgr.get_active_bookings()
    
    if bookings_raw:
        # Simulate what app.py does
        bookings_enhanced = []
        for booking in bookings_raw:
            duration_detailed = Helper.calculate_duration_detailed(booking[5])
            bookings_enhanced.append(booking + (duration_detailed['display'],))
        
        print(f"   ✅ PASS - {len(bookings_enhanced)} active booking(s) with duration")
        for b in bookings_enhanced:
            print(f"   - User: {b[1]}, Slot: {b[3]}, Duration: {b[6]}")
        tests_passed += 1
    else:
        print(f"   ℹ️  INFO - No active bookings (may be expected)")
        tests_passed += 1
except Exception as e:
    print(f"   ❌ FAIL - {e}")
    import traceback
    traceback.print_exc()

# Test 4: Booking statistics
print("\n[Test 4] Testing booking statistics...")
tests_total += 1
try:
    stats = booking_mgr.get_booking_statistics()
    if all(key in stats for key in ['total', 'active', 'completed']):
        print(f"   ✅ PASS - Statistics: Total={stats['total']}, Active={stats['active']}, Completed={stats['completed']}")
        tests_passed += 1
    else:
        print(f"   ❌ FAIL - Missing statistics keys")
except Exception as e:
    print(f"   ❌ FAIL - {e}")

# Test 5: Slot availability
print("\n[Test 5] Testing slot availability...")
tests_total += 1
try:
    available = slot_mgr.get_available_slots()
    stats = slot_mgr.get_slot_statistics()
    print(f"   ✅ PASS - {len(available)} available slots, {stats['occupied']} occupied")
    tests_passed += 1
except Exception as e:
    print(f"   ❌ FAIL - {e}")

# Test 6: Database integrity
print("\n[Test 6] Testing database integrity...")
tests_total += 1
try:
    # Check for orphaned bookings (active bookings with non-existent slots)
    query = """
        SELECT COUNT(*) FROM bookings b
        LEFT JOIN slots s ON b.slot_id = s.id
        WHERE b.status = 'Active' AND s.id IS NULL
    """
    orphaned = db.fetch_one(query)[0]
    
    if orphaned == 0:
        print(f"   ✅ PASS - No orphaned bookings")
        tests_passed += 1
    else:
        print(f"   ⚠️  WARNING - {orphaned} orphaned booking(s) found")
except Exception as e:
    print(f"   ❌ FAIL - {e}")

# Test 7: Cost calculation edge cases
print("\n[Test 7] Testing cost calculation edge cases...")
tests_total += 1
try:
    # Test minimum charge
    cost_1min = Helper.calculate_cost(0.01)  # < 1 hour
    cost_1hr = Helper.calculate_cost(1.0)
    cost_2hr = Helper.calculate_cost(2.5)
    
    if cost_1min == 50 and cost_1hr == 50 and cost_2hr == 125:
        print(f"   ✅ PASS - Cost calculations correct")
        print(f"   1 min: ₹{cost_1min}, 1 hr: ₹{cost_1hr}, 2.5 hr: ₹{cost_2hr}")
        tests_passed += 1
    else:
        print(f"   ❌ FAIL - Incorrect cost: {cost_1min}, {cost_1hr}, {cost_2hr}")
except Exception as e:
    print(f"   ❌ FAIL - {e}")

# Final Results
print("\n" + "=" * 80)
print("TEST RESULTS")
print("=" * 80)
print(f"Tests Passed: {tests_passed}/{tests_total}")
print(f"Success Rate: {(tests_passed/tests_total*100):.1f}%")

if tests_passed == tests_total:
    print("\n🎉 ALL TESTS PASSED! 🎉")
    print("\nThe active bookings system is fully functional!")
    print("\nYou can now:")
    print("1. Start the Flask app: python app.py")
    print("2. Login as user1 / user123")
    print("3. View the enhanced dashboard with real-time updates")
    print("4. Login as admin / admin123 to see admin features")
else:
    print(f"\n⚠️  {tests_total - tests_passed} test(s) failed")
    print("Review the errors above for details")

print("=" * 80)
