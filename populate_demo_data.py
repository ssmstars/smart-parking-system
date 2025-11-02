"""
Demo Data Script
Populates the database with sample parking slots for testing
"""

from modules.slot_manager import SlotManager


def populate_demo_slots():
    """Add sample parking slots to the system"""
    slot_manager = SlotManager()
    
    print("=" * 60)
    print("🅿️  POPULATING DEMO PARKING SLOTS")
    print("=" * 60)
    
    # Floor 1 - Regular slots
    regular_slots_f1 = ['A1', 'A2', 'A3', 'A4', 'A5', 'B1', 'B2', 'B3', 'B4', 'B5']
    
    print("\nAdding Floor 1 - Regular Slots...")
    for slot in regular_slots_f1:
        result = slot_manager.add_slot(slot, 'Regular', 1)
        if result['success']:
            print(f"  ✓ Added slot {slot}")
        else:
            print(f"  ✗ Failed: {slot} - {result['message']}")
    
    # Floor 1 - VIP slots
    vip_slots_f1 = ['VIP1', 'VIP2', 'VIP3']
    
    print("\nAdding Floor 1 - VIP Slots...")
    for slot in vip_slots_f1:
        result = slot_manager.add_slot(slot, 'VIP', 1)
        if result['success']:
            print(f"  ✓ Added slot {slot}")
        else:
            print(f"  ✗ Failed: {slot} - {result['message']}")
    
    # Floor 1 - Handicapped slots
    handicapped_slots = ['H1', 'H2']
    
    print("\nAdding Floor 1 - Handicapped Slots...")
    for slot in handicapped_slots:
        result = slot_manager.add_slot(slot, 'Handicapped', 1)
        if result['success']:
            print(f"  ✓ Added slot {slot}")
        else:
            print(f"  ✗ Failed: {slot} - {result['message']}")
    
    # Floor 2 - Regular slots
    regular_slots_f2 = ['C1', 'C2', 'C3', 'C4', 'C5', 'D1', 'D2', 'D3', 'D4', 'D5']
    
    print("\nAdding Floor 2 - Regular Slots...")
    for slot in regular_slots_f2:
        result = slot_manager.add_slot(slot, 'Regular', 2)
        if result['success']:
            print(f"  ✓ Added slot {slot}")
        else:
            print(f"  ✗ Failed: {slot} - {result['message']}")
    
    # Floor 2 - EV Charging slots
    ev_slots = ['EV1', 'EV2', 'EV3']
    
    print("\nAdding Floor 2 - EV Charging Slots...")
    for slot in ev_slots:
        result = slot_manager.add_slot(slot, 'EV Charging', 2)
        if result['success']:
            print(f"  ✓ Added slot {slot}")
        else:
            print(f"  ✗ Failed: {slot} - {result['message']}")
    
    # Get statistics
    stats = slot_manager.get_slot_statistics()
    
    print("\n" + "=" * 60)
    print("📊 PARKING STATISTICS")
    print("=" * 60)
    print(f"Total Slots Created: {stats['total']}")
    print(f"Available Slots: {stats['available']}")
    print(f"Occupied Slots: {stats['occupied']}")
    print(f"Occupancy Rate: {stats['occupancy_rate']}%")
    print("=" * 60)
    print("\n✅ Demo data populated successfully!")
    print("You can now login and test the system.\n")


if __name__ == "__main__":
    populate_demo_slots()
