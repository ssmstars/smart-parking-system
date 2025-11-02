# 🚀 Quick Start Guide - Smart Parking System

## ⚡ Getting Started in 3 Steps

### Step 1: Populate Demo Data (Optional but Recommended)
```bash
python populate_demo_data.py
```
This will create 33 parking slots across 2 floors with different types.

### Step 2: Run the Application
```bash
python main.py
```

### Step 3: Login and Explore

## 🔑 Login Credentials

### Admin Login
- **Username**: `admin`
- **Password**: `admin123`

**What you can do as Admin:**
- Add/Delete parking slots
- View all bookings
- Monitor real-time statistics
- Manage system settings

### User Login
**First-time users need to register:**
1. Click "New User? Register Here"
2. Fill in all required fields:
   - Username (3-20 characters, alphanumeric)
   - Password (minimum 6 characters)
   - Email (valid email format)
   - Phone (10 digits)
   - Vehicle Number (e.g., MH12AB1234)
3. Click "REGISTER"
4. Login with your new credentials

**What you can do as User:**
- View available parking slots
- Book a parking slot
- Cancel/checkout from parking
- View booking history
- Track parking duration and cost

## 📱 Sample Test Workflow

### Testing as Admin:
1. Login as admin
2. View the 33 demo slots in "Manage Slots" tab
3. Check statistics dashboard
4. View bookings (will be empty initially)
5. Add more slots if needed in "Add New Slot" tab

### Testing as User:
1. Register a new user account (e.g., username: `john`, password: `john123`)
2. Login with your credentials
3. Go to "Book Parking Slot" tab
4. Select an available slot (e.g., A1, VIP1, etc.)
5. Verify/update vehicle number
6. Click "BOOK SELECTED SLOT"
7. Dashboard will show your active parking with:
   - Slot details
   - Check-in time
   - Current duration
   - Estimated cost
8. To checkout: Click "CHECKOUT & CANCEL BOOKING"
9. View receipt with final cost
10. Check "My Booking History" for past bookings

## 🎯 Quick Feature Demo

### Booking Flow:
```
Register User → Login → Select Slot → Book → View Status → Checkout
```

### Admin Flow:
```
Login → View Statistics → Manage Slots → Monitor Bookings
```

## 💡 Tips

1. **Multiple Users**: Register multiple user accounts to test concurrent bookings
2. **Different Slot Types**: Book different types of slots (Regular, VIP, EV, Handicapped)
3. **Floor Management**: Notice slots are organized by floors
4. **Cost Calculation**: Leave a booking active for a few minutes to see duration increase
5. **History**: Cancel and re-book to build up booking history

## 🛠️ Customization

### Change Parking Rate:
Edit `utils/helpers.py` → `calculate_cost()` function
```python
def calculate_cost(hours, rate_per_hour=50):  # Change 50 to your rate
```

### Add More Slot Types:
Edit `ui/admin_dashboard.py` → `create_add_slot_tab()` function
```python
values=['Regular', 'VIP', 'Handicapped', 'EV Charging', 'YourNewType']
```

## 📊 System Demo Data

After running `populate_demo_data.py`, you'll have:

**Floor 1:**
- 10 Regular slots (A1-A5, B1-B5)
- 3 VIP slots (VIP1-VIP3)
- 2 Handicapped slots (H1-H2)

**Floor 2:**
- 10 Regular slots (C1-C5, D1-D5)
- 3 EV Charging slots (EV1-EV3)

**Total:** 33 parking slots

## ❓ Common Questions

**Q: Can I book multiple slots at once?**
A: No, each user can have only one active booking at a time.

**Q: What happens if I close the app during active booking?**
A: Your booking remains active in the database. Login again to checkout.

**Q: Can I delete a slot that's occupied?**
A: No, admin cannot delete slots with active bookings.

**Q: How is cost calculated?**
A: ₹50/hour, minimum charge ₹50 (even for <1 hour)

**Q: Can I change my vehicle number?**
A: Yes, you can update it before booking. To change registered vehicle, admin needs to update the database.

## 🐛 Troubleshooting

**Problem**: "Module not found" error
**Solution**: Make sure you're in the project directory: `cd "e:\smart parking system"`

**Problem**: Database locked error
**Solution**: Close all running instances of the application

**Problem**: Tkinter not found
**Solution**: Tkinter comes with Python. Reinstall Python with "tcl/tk" option enabled.

## 🎉 Enjoy!

You now have a fully functional Smart Parking System!

Test all features and customize as needed.

---
**Happy Parking! 🚗🅿️**
