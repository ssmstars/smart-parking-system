"""
Flask Web Application for Smart Parking System
Main application file
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
import os
from datetime import datetime, timedelta

# Import existing modules
from modules.authentication import Authentication
from modules.slot_manager import SlotManager
from modules.booking_manager import BookingManager
from utils.helpers import Helper

app = Flask(__name__)
app.secret_key = 'smart_parking_secret_key_2025'  # Change this in production

# Initialize managers
auth = Authentication()
slot_manager = SlotManager()
booking_manager = BookingManager()


# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Admin access required', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# Routes
@app.route('/')
def index():
    """Home page"""
    if 'user_id' in session:
        if session.get('role') == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'user')
        
        if role == 'admin':
            result = auth.admin_login(username, password)
        else:
            result = auth.user_login(username, password)
        
        if result['success']:
            session['user_id'] = result['user_id']
            session['username'] = result['username']
            session['role'] = result['role']
            flash(f'Welcome back, {result["username"]}!', 'success')
            
            if role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            flash(result['message'], 'danger')
    
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        phone = request.form.get('phone')
        vehicle_number = request.form.get('vehicle_number')
        
        result = auth.register_user(username, password, email, phone, vehicle_number)
        
        if result['success']:
            flash(result['message'], 'success')
            return redirect(url_for('login'))
        else:
            flash(result['message'], 'danger')
    
    return render_template('register.html')


@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


# Admin Routes
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    stats = slot_manager.get_slot_statistics()
    booking_stats = booking_manager.get_booking_statistics()
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         booking_stats=booking_stats)


@app.route('/admin/slots')
@admin_required
def admin_slots():
    """Manage slots"""
    slots = slot_manager.get_all_slots()
    return render_template('admin/slots.html', slots=slots)


@app.route('/admin/slots/add', methods=['POST'])
@admin_required
def add_slot():
    """Add new slot"""
    slot_number = request.form.get('slot_number')
    slot_type = request.form.get('slot_type')
    floor = request.form.get('floor')
    
    result = slot_manager.add_slot(slot_number, slot_type, int(floor))
    
    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'danger')
    
    return redirect(url_for('admin_slots'))


@app.route('/admin/slots/delete/<int:slot_id>', methods=['POST'])
@admin_required
def delete_slot(slot_id):
    """Delete slot"""
    result = slot_manager.delete_slot(slot_id)
    
    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(result['message'], 'danger')
    
    return redirect(url_for('admin_slots'))


@app.route('/admin/bookings')
@admin_required
def admin_bookings():
    """View all bookings"""
    filter_type = request.args.get('filter', 'all')
    
    if filter_type == 'active':
        bookings_raw = booking_manager.get_active_bookings()
        # Add duration calculation for active bookings
        bookings = []
        for booking in bookings_raw:
            # booking structure: id, username, phone, slot_number, vehicle_number, booking_time
            duration = Helper.calculate_duration(booking[5])
            duration_detailed = Helper.calculate_duration_detailed(booking[5])
            # Add duration as 7th element
            bookings.append(booking + (duration_detailed['display'],))
    else:
        bookings = booking_manager.get_all_bookings()
    
    return render_template('admin/bookings.html', bookings=bookings, filter_type=filter_type)


# User Routes
@app.route('/user/dashboard')
@login_required
def user_dashboard():
    """User dashboard"""
    user_id = session.get('user_id')
    username = session.get('username')
    
    print(f"DEBUG: Dashboard accessed by User ID: {user_id}, Username: {username}")
    
    # Get active booking
    active_booking = booking_manager.get_active_booking(user_id)
    print(f"DEBUG: Active booking for user {user_id}: {active_booking}")
    
    # Calculate duration and cost if active booking exists
    booking_info = None
    if active_booking:
        duration = Helper.calculate_duration(active_booking[4])
        cost = Helper.calculate_cost(duration)
        
        booking_info = {
            'id': active_booking[0],
            'slot_number': active_booking[1],
            'slot_type': active_booking[2],
            'vehicle_number': active_booking[3],
            'booking_time': Helper.format_datetime(active_booking[4]),
            'booking_time_raw': active_booking[4],  # For JavaScript
            'floor': active_booking[5],
            'duration': duration,
            'cost': cost
        }
    
    # Get available slots count
    available_slots = slot_manager.get_available_slots()
    
    return render_template('user/dashboard.html', 
                         booking=booking_info,
                         available_count=len(available_slots))


@app.route('/user/book-slot', methods=['GET', 'POST'])
@login_required
def book_slot():
    """Book parking slot"""
    if request.method == 'POST':
        try:
            user_id = session.get('user_id')
            slot_id = request.form.get('slot_id')
            vehicle_number = request.form.get('vehicle_number')
            
            # Validate inputs
            if not slot_id:
                flash('Please select a parking slot', 'danger')
                return redirect(url_for('book_slot'))
            
            if not vehicle_number:
                flash('Please enter vehicle number', 'danger')
                return redirect(url_for('book_slot'))
            
            # Get package
            package = request.form.get('package', 'hourly')
            
            # Get booking time option
            booking_time_option = request.form.get('booking_time_option', 'now')
            
            # Handle date/time based on user selection
            if booking_time_option == 'custom':
                booking_date = request.form.get('booking_date')
                booking_time = request.form.get('booking_time')
                
                if not booking_date or not booking_time:
                    flash('Please select both date and time for scheduled booking', 'danger')
                    return redirect(url_for('book_slot'))
            else:
                # Use current time for immediate booking
                booking_date = None
                booking_time = None
            
            print(f"DEBUG: Booking attempt - User: {user_id}, Slot: {slot_id}, Vehicle: {vehicle_number}, Package: {package}, Time Option: {booking_time_option}")
            
            result = booking_manager.book_slot(
                user_id, 
                int(slot_id), 
                vehicle_number,
                booking_date=booking_date,
                booking_time=booking_time,
                package=package
            )
            
            print(f"DEBUG: Booking result - {result}")
            
            if result['success']:
                flash(result['message'], 'success')
                return redirect(url_for('user_dashboard'))
            else:
                flash(result['message'], 'danger')
                return redirect(url_for('book_slot'))
        except Exception as e:
            print(f"ERROR in book_slot: {str(e)}")
            import traceback
            traceback.print_exc()
            flash(f'Booking error: {str(e)}', 'danger')
            return redirect(url_for('book_slot'))
    
    # Get user's saved vehicle number
    user_id = session.get('user_id')
    user_query = "SELECT vehicle_number FROM users WHERE id = ?"
    user_data = auth.db.fetch_one(user_query, (user_id,))
    saved_vehicle = user_data[0] if user_data and user_data[0] else None
    
    # Get available slots grouped by floor
    available_slots = slot_manager.get_available_slots()
    
    # Group by floor
    slots_by_floor = {}
    for slot in available_slots:
        floor = slot[3]
        if floor not in slots_by_floor:
            slots_by_floor[floor] = []
        slots_by_floor[floor].append({
            'id': slot[0],
            'slot_number': slot[1],
            'slot_type': slot[2],
            'floor': slot[3]
        })
    
    # Get floors list
    floors = sorted(slots_by_floor.keys())
    
    return render_template('user/book_slot.html', 
                         slots_by_floor=slots_by_floor,
                         floors=floors,
                         saved_vehicle=saved_vehicle)


@app.route('/user/cancel-booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    """Cancel/checkout booking"""
    try:
        user_id = session.get('user_id')
        
        print(f"DEBUG: Cancel booking attempt - User: {user_id}, Booking ID: {booking_id}")
        
        result = booking_manager.cancel_booking(booking_id, user_id)
        
        print(f"DEBUG: Cancel result - {result}")
        
        if result['success']:
            # Display comprehensive checkout information
            message = f"{result['message']} Duration: {result['duration']:.2f} hours, Final Cost: ₹{result['actual_cost']:.2f}"
            if result.get('package_cost'):
                message += f" (Package: {result['package']} - ₹{result['package_cost']:.2f})"
            flash(message, 'success')
        else:
            flash(result['message'], 'danger')
        
        return redirect(url_for('user_dashboard'))
    except Exception as e:
        print(f"ERROR in cancel_booking: {str(e)}")
        import traceback
        traceback.print_exc()
        flash(f'Checkout error: {str(e)}', 'danger')
        return redirect(url_for('user_dashboard'))


@app.route('/user/bookings')
@login_required
def user_bookings():
    """View booking history"""
    user_id = session.get('user_id')
    bookings = booking_manager.get_user_bookings(user_id)
    
    # Format bookings
    formatted_bookings = []
    for booking in bookings:
        formatted_bookings.append({
            'id': booking[0],
            'slot_number': booking[1],
            'slot_type': booking[2],
            'vehicle_number': booking[3],
            'booking_time': Helper.format_datetime(booking[4]),
            'checkout_time': Helper.format_datetime(booking[5]) if booking[5] else 'Active',
            'status': booking[6]
        })
    
    return render_template('user/bookings.html', bookings=formatted_bookings)


# API Routes for AJAX
# API Routes for AJAX
@app.route('/api/booking/active')
@login_required
def get_active_booking_api():
    """Get active booking data (AJAX)"""
    user_id = session.get('user_id')
    active_booking = booking_manager.get_active_booking(user_id)
    
    if active_booking:
        duration = Helper.calculate_duration(active_booking[4])
        cost = Helper.calculate_cost(duration)
        
        return jsonify({
            'success': True,
            'booking': {
                'id': active_booking[0],
                'slot_number': active_booking[1],
                'slot_type': active_booking[2],
                'vehicle_number': active_booking[3],
                'booking_time': active_booking[4],
                'booking_time_formatted': Helper.format_datetime(active_booking[4]),
                'floor': active_booking[5],
                'duration': duration,
                'cost': cost
            }
        })
    else:
        return jsonify({'success': False, 'message': 'No active booking'})


@app.route('/api/slots/floor/<int:floor>')
@login_required
def get_slots_by_floor(floor):
    """Get slots by floor (AJAX)"""
    available_slots = slot_manager.get_available_slots()
    
    floor_slots = [
        {
            'id': slot[0],
            'slot_number': slot[1],
            'slot_type': slot[2],
            'floor': slot[3]
        }
        for slot in available_slots if slot[3] == floor
    ]
    
    return jsonify(floor_slots)


@app.route('/api/stats')
@admin_required
def get_stats():
    """Get statistics (AJAX)"""
    stats = slot_manager.get_slot_statistics()
    booking_stats = booking_manager.get_booking_statistics()
    
    return jsonify({
        'slots': stats,
        'bookings': booking_stats
    })


# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
