"""
Parking Slot Management Module
Handles all parking slot operations (Admin)
"""

from database.db_manager import DatabaseManager
from utils.validators import Validator


class SlotManager:
    """Manages parking slot operations"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def add_slot(self, slot_number, slot_type='Regular', floor=1):
        """Add new parking slot"""
        if not Validator.validate_slot_number(slot_number):
            return {'success': False, 'message': 'Invalid slot number format.'}
        
        slot_number = slot_number.upper()
        
        # Check if slot already exists
        check_query = "SELECT id FROM slots WHERE slot_number = ?"
        existing = self.db.fetch_one(check_query, (slot_number,))
        
        if existing:
            return {'success': False, 'message': 'Slot number already exists.'}
        
        # Insert new slot
        insert_query = """
            INSERT INTO slots (slot_number, slot_type, status, floor)
            VALUES (?, ?, 'Available', ?)
        """
        success = self.db.execute_query(insert_query, (slot_number, slot_type, floor))
        
        if success:
            return {'success': True, 'message': f'Slot {slot_number} added successfully.'}
        return {'success': False, 'message': 'Failed to add slot.'}
    
    def update_slot(self, slot_id, slot_number=None, slot_type=None, floor=None):
        """Update existing slot"""
        updates = []
        params = []
        
        if slot_number:
            if not Validator.validate_slot_number(slot_number):
                return {'success': False, 'message': 'Invalid slot number format.'}
            updates.append("slot_number = ?")
            params.append(slot_number.upper())
        
        if slot_type:
            updates.append("slot_type = ?")
            params.append(slot_type)
        
        if floor:
            updates.append("floor = ?")
            params.append(floor)
        
        if not updates:
            return {'success': False, 'message': 'No updates provided.'}
        
        params.append(slot_id)
        update_query = f"UPDATE slots SET {', '.join(updates)} WHERE id = ?"
        
        success = self.db.execute_query(update_query, tuple(params))
        
        if success:
            return {'success': True, 'message': 'Slot updated successfully.'}
        return {'success': False, 'message': 'Failed to update slot.'}
    
    def delete_slot(self, slot_id):
        """Delete parking slot"""
        # Check if slot has active bookings
        check_query = "SELECT COUNT(*) FROM bookings WHERE slot_id = ? AND status = 'Active'"
        result = self.db.fetch_one(check_query, (slot_id,))
        
        if result and result[0] > 0:
            return {'success': False, 'message': 'Cannot delete slot with active bookings.'}
        
        delete_query = "DELETE FROM slots WHERE id = ?"
        success = self.db.execute_query(delete_query, (slot_id,))
        
        if success:
            return {'success': True, 'message': 'Slot deleted successfully.'}
        return {'success': False, 'message': 'Failed to delete slot.'}
    
    def get_all_slots(self):
        """Get all parking slots"""
        query = "SELECT id, slot_number, slot_type, status, floor, created_at FROM slots ORDER BY slot_number"
        return self.db.fetch_all(query)
    
    def get_available_slots(self):
        """Get all available parking slots"""
        query = """
            SELECT id, slot_number, slot_type, floor 
            FROM slots 
            WHERE status = 'Available' 
            ORDER BY slot_number
        """
        return self.db.fetch_all(query)
    
    def get_slot_by_id(self, slot_id):
        """Get slot details by ID"""
        query = "SELECT id, slot_number, slot_type, status, floor FROM slots WHERE id = ?"
        return self.db.fetch_one(query, (slot_id,))
    
    def get_slot_statistics(self):
        """Get parking slot statistics"""
        total_query = "SELECT COUNT(*) FROM slots"
        available_query = "SELECT COUNT(*) FROM slots WHERE status = 'Available'"
        occupied_query = "SELECT COUNT(*) FROM slots WHERE status = 'Occupied'"
        
        total = self.db.fetch_one(total_query)[0]
        available = self.db.fetch_one(available_query)[0]
        occupied = self.db.fetch_one(occupied_query)[0]
        
        return {
            'total': total,
            'available': available,
            'occupied': occupied,
            'occupancy_rate': round((occupied / total * 100) if total > 0 else 0, 2)
        }
    
    def update_slot_status(self, slot_id, status):
        """Update slot status (Available/Occupied)"""
        update_query = "UPDATE slots SET status = ? WHERE id = ?"
        success = self.db.execute_query(update_query, (status, slot_id))
        return success
