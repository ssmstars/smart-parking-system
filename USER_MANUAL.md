# 📖 User Manual - Smart Parking System

## Complete Guide for Users and Administrators

---

## 📑 Table of Contents

1. [Getting Started](#getting-started)
2. [Admin Guide](#admin-guide)
3. [User Guide](#user-guide)
4. [Common Tasks](#common-tasks)
5. [Troubleshooting](#troubleshooting)
6. [FAQ](#faq)

---

## 🚀 Getting Started

### System Requirements

- **Operating System**: Windows 7/10/11, macOS 10.12+, or Linux
- **Python**: Version 3.7 or higher
- **RAM**: Minimum 512 MB
- **Storage**: 50 MB free space
- **Display**: 1024x768 resolution or higher

### Installation

1. **Ensure Python is installed**
   ```bash
   python --version
   ```
   Should show Python 3.7 or higher

2. **Navigate to project directory**
   ```bash
   cd "e:\smart parking system"
   ```

3. **Populate demo data** (Optional but recommended for first-time use)
   ```bash
   python populate_demo_data.py
   ```
   This creates 33 sample parking slots

4. **Run the application**
   ```bash
   python main.py
   ```

### First Launch

When you first run the application:
1. The database is automatically created
2. Default admin account is created
3. The login window appears

---

## 👨‍💼 Admin Guide

### Logging In as Admin

1. **Launch the application**
   ```bash
   python main.py
   ```

2. **Select "Admin" role** on login screen

3. **Enter credentials**
   - Username: `admin`
   - Password: `admin123`

4. **Click "LOGIN"** button

### Admin Dashboard Overview

After login, you'll see:

#### 📊 Statistics Dashboard (Top)
Four real-time statistics cards:
- **Total Slots**: Total number of parking slots
- **Available**: Number of free slots
- **Occupied**: Number of slots in use
- **Active Bookings**: Current active bookings

#### 🗂️ Tabbed Interface
Three main tabs:
1. Manage Slots
2. View Bookings
3. Add New Slot

---

### Managing Parking Slots

#### ➕ Adding New Slots

1. **Navigate to "Add New Slot" tab**

2. **Fill in the form**:
   - **Slot Number**: Unique identifier (e.g., A1, B2, VIP1)
     - 1-10 characters
     - Letters and numbers only
     - Will be converted to uppercase
   
   - **Slot Type**: Select from dropdown
     - Regular (standard parking)
     - VIP (premium parking)
     - Handicapped (accessible parking)
     - EV Charging (electric vehicle)
   
   - **Floor**: Select floor number (1-10)

3. **Click "ADD SLOT"** button

4. **Success message** confirms slot creation

5. **Click "CLEAR"** to reset form for next entry

**Tips:**
- Use consistent naming (A1, A2, A3 or P1, P2, P3)
- Organize by floor (Floor 1: A1-A10, Floor 2: B1-B10)
- Reserve slot types appropriately

#### ✏️ Viewing All Slots

1. **Navigate to "Manage Slots" tab**

2. **Slot List displays**:
   - ID (database identifier)
   - Slot Number
   - Type (Regular, VIP, etc.)
   - Status (Available or Occupied)
   - Floor
   - Created At (timestamp)

3. **Color Coding**:
   - 🟢 Green background = Available
   - 🔴 Red background = Occupied

4. **Click "Refresh"** to update the list

#### 🗑️ Deleting Slots

1. **Navigate to "Manage Slots" tab**

2. **Select a slot** from the list (click on it)

3. **Click "Delete Selected"** button

4. **Confirm deletion** in popup dialog

**Important:**
- ❌ Cannot delete occupied slots
- ⚠️ Deletion is permanent
- ✅ Recommended: Only delete slots not in use

---

### Viewing Bookings

#### 📋 All Bookings View

1. **Navigate to "View Bookings" tab**

2. **Click "Show All"** to see all bookings

3. **Booking List displays**:
   - Booking ID
   - Username (who booked)
   - Slot Number
   - Vehicle Number
   - Booking Time
   - Checkout Time
   - Status (Active/Completed)

4. **Color Coding**:
   - 🟡 Yellow background = Active booking
   - 🟢 Green background = Completed booking

#### 🔍 Active Bookings Only

1. **Click "Active Only"** button

2. **Shows only current active bookings**:
   - User details
   - Phone number
   - Slot number
   - Vehicle number
   - Booking time

3. **Useful for**:
   - Quick overview of occupancy
   - Contact information for users
   - Current parking status

#### 🔄 Refreshing Data

- **Click "Refresh"** button anytime to update data
- Auto-refresh not enabled (manual refresh required)

---

### Admin Best Practices

✅ **Do's:**
- Regularly monitor booking statistics
- Keep slot numbering consistent
- Review completed bookings periodically
- Maintain appropriate slot type distribution
- Use clear slot numbering system

❌ **Don'ts:**
- Don't delete occupied slots
- Avoid duplicate slot numbers
- Don't share admin credentials
- Don't delete all slots (keep system operational)

---

## 🚗 User Guide

### Creating an Account

#### First-Time Registration

1. **Launch the application**

2. **Click "New User? Register Here"** button

3. **Fill in registration form**:
   
   - **Username** (required)
     - 3-20 characters
     - Letters, numbers, underscore only
     - Must be unique
     - Example: `john_doe`, `user123`
   
   - **Password** (required)
     - Minimum 6 characters
     - Case-sensitive
     - Remember it securely
   
   - **Email** (required)
     - Valid email format
     - Must be unique
     - Example: `john@email.com`
   
   - **Phone Number** (required)
     - Exactly 10 digits
     - Numbers only
     - Example: `9876543210`
   
   - **Vehicle Number** (required)
     - 4-15 characters
     - Letters, numbers, hyphen only
     - Will be converted to uppercase
     - Example: `MH12AB1234`, `DL01CD5678`

4. **Click "REGISTER"** button

5. **Success message** confirms registration

6. **Click "Cancel"** to return to login

7. **Login with your new credentials**

**Common Registration Errors:**
- ❌ Username already exists → Choose different username
- ❌ Email already exists → Use different email
- ❌ Invalid email format → Check email syntax
- ❌ Phone not 10 digits → Enter exactly 10 digits
- ❌ Invalid vehicle format → Use letters and numbers only

---

### Logging In as User

1. **Select "User" role** on login screen

2. **Enter your credentials**:
   - Username
   - Password

3. **Click "LOGIN"** button

4. **User dashboard opens**

---

### User Dashboard Overview

After login, you'll see:

#### 🅿️ Current Parking Status (Top)

**If you have active parking:**
- Slot number and type
- Vehicle number
- Floor number
- Check-in time
- Current duration (hours)
- Estimated cost (₹)
- "CHECKOUT & CANCEL BOOKING" button

**If no active parking:**
- "No Active Parking" message
- "Book a slot to start parking" prompt

#### 🗂️ Tabbed Interface
Two main tabs:
1. Book Parking Slot
2. My Booking History

---

### Booking a Parking Slot

#### 📍 Step-by-Step Booking Process

1. **Navigate to "Book Parking Slot" tab**

2. **View available slots**:
   - List shows all free parking slots
   - Columns: ID, Slot Number, Type, Floor
   - Organized by slot number

3. **Select desired slot**:
   - Click on any slot in the list
   - Consider:
     - Slot type (Regular, VIP, Handicapped, EV)
     - Floor preference
     - Location convenience

4. **Verify vehicle number**:
   - Pre-filled from registration
   - Can be updated if needed
   - Will be converted to uppercase

5. **Click "BOOK SELECTED SLOT"** button

6. **Confirm booking** in popup dialog

7. **Success message** shows slot number

8. **Status updates**:
   - Slot disappears from available list
   - Current parking status shows your booking
   - Duration tracking begins

**Booking Rules:**
- ✅ One active booking per user
- ✅ Can only book available slots
- ❌ Cannot book if you have active parking
- ❌ Cannot book already occupied slots

#### 🔄 Refreshing Available Slots

- **Click "Refresh"** button to update list
- Shows real-time availability
- Useful if someone else books while you're viewing

---

### Checking Out (Cancelling Booking)

#### 🚪 Checkout Process

1. **View your current parking** in status section

2. **Note the details**:
   - Duration (hours parked)
   - Estimated cost

3. **Click "CHECKOUT & CANCEL BOOKING"** button

4. **Confirm checkout** in popup dialog

5. **Receipt shows**:
   - Slot number
   - Total duration (hours)
   - Final cost (₹)

6. **Slot becomes available** again

7. **Booking moves to history** as "Completed"

#### 💰 Cost Calculation

- **Rate**: ₹50 per hour
- **Minimum charge**: ₹50 (even if less than 1 hour)
- **Examples**:
  - 30 minutes = ₹50
  - 1.5 hours = ₹75
  - 3 hours = ₹150

**Cost Formula:**
```
If duration < 1 hour: Cost = ₹50
If duration ≥ 1 hour: Cost = duration × ₹50
```

---

### Viewing Booking History

#### 📜 My Booking History

1. **Navigate to "My Booking History" tab**

2. **View all your bookings**:
   - Booking ID
   - Slot Number
   - Slot Type
   - Vehicle Number
   - Booking Time (check-in)
   - Checkout Time (if completed)
   - Status (Active/Completed)

3. **Color Coding**:
   - 🟡 Yellow = Active (current parking)
   - 🟢 Green = Completed (past bookings)

4. **Click "Refresh"** to update list

**Uses:**
- Track parking patterns
- Review past costs
- Verify booking history
- Check parking duration trends

---

### User Best Practices

✅ **Do's:**
- Book slots appropriate to your vehicle type
- Checkout promptly when leaving
- Keep vehicle number updated
- Review booking history regularly
- Note your slot number and floor

❌ **Don'ts:**
- Don't leave bookings active when not parked
- Don't share your login credentials
- Don't book slots you won't use
- Don't forget your slot location

---

## 🔧 Common Tasks

### Task 1: Bulk Adding Slots (Admin)

**Scenario:** Need to add 10 regular slots on Floor 1

**Solution:**
1. Go to "Add New Slot" tab
2. Add slot A1, Type: Regular, Floor: 1
3. Click "ADD SLOT"
4. Click "CLEAR"
5. Repeat for A2, A3... A10
6. Check "Manage Slots" to verify all added

**Tip:** Use populate_demo_data.py for bulk creation

---

### Task 2: Finding Available VIP Slots (User)

**Scenario:** Need a VIP parking slot

**Solution:**
1. Go to "Book Parking Slot" tab
2. Look for slots with Type: "VIP"
3. Note the slot number and floor
4. Select and book
5. Remember the floor for easy parking

---

### Task 3: Checking Total Parking Cost (User)

**Scenario:** Want to know current parking cost

**Solution:**
1. View top status section
2. Look at "Estimated Cost" line
3. Shows real-time calculation
4. Updates as duration increases
5. Final cost shown at checkout

---

### Task 4: Monitoring Occupancy (Admin)

**Scenario:** Check how full the parking is

**Solution:**
1. View statistics dashboard at top
2. Check "Occupied" vs "Total Slots"
3. Calculate: (Occupied/Total) × 100%
4. Or use "Occupancy Rate" from populate script
5. Review "Active Bookings" for current users

---

### Task 5: Recovering from Accidental Logout (User)

**Scenario:** Closed app with active booking

**Solution:**
1. Reopen application
2. Login with same credentials
3. Your booking is preserved
4. Status shows active parking
5. Continue as normal or checkout

---

## 🔍 Troubleshooting

### Problem: "Database not found"

**Symptoms:** Error on startup about missing database

**Solution:**
- Database is auto-created on first run
- Ensure you have write permissions in folder
- Check disk space available
- Run from correct directory

---

### Problem: "Cannot delete slot"

**Symptoms:** Error when trying to delete slot

**Possible Causes:**
1. Slot is currently occupied
2. Slot has active booking

**Solution:**
- Check slot status (should be Available)
- Wait for user to checkout
- View "Active Bookings" to find who has it
- Only delete Available slots

---

### Problem: "Username already exists"

**Symptoms:** Cannot register new user

**Solution:**
- Choose a different username
- Usernames must be unique
- Try adding numbers (john → john123)
- Or use underscores (john → john_doe)

---

### Problem: "You already have an active booking"

**Symptoms:** Cannot book new slot

**Solution:**
- You can only have one active booking
- Check current parking status
- Checkout from current booking first
- Then book new slot

---

### Problem: "Invalid vehicle number"

**Symptoms:** Registration or booking fails

**Solution:**
- Use 4-15 characters
- Letters, numbers, and hyphens only
- No spaces or special characters
- Examples: MH12AB1234, DL-01-CD-5678

---

### Problem: Application won't start

**Symptoms:** Window doesn't open

**Checklist:**
1. Python installed? (`python --version`)
2. Tkinter available? (comes with Python)
3. In correct directory?
4. No syntax errors in code?
5. Try from terminal to see errors

**Windows:**
```bash
cd "e:\smart parking system"
python main.py
```

**Mac/Linux:**
```bash
cd "e:/smart parking system"
python3 main.py
```

---

### Problem: Slots not showing

**Symptoms:** Empty slots list

**Solution:**
- No slots added yet
- Run `python populate_demo_data.py`
- Or manually add slots via "Add New Slot"
- Click "Refresh" button

---

### Problem: Forgot admin password

**Symptoms:** Cannot login as admin

**Solution:**
1. Delete `smart_parking.db` file
2. Restart application
3. Default admin recreated automatically
4. Login with admin/admin123
5. **Warning:** This deletes all data!

---

## ❓ FAQ

### General Questions

**Q1: Is internet required?**
A: No, the system works completely offline.

**Q2: Can multiple users login simultaneously?**
A: Not in current version. It's a single-user GUI application.

**Q3: Where is data stored?**
A: In `smart_parking.db` SQLite file in the project folder.

**Q4: Can I backup my data?**
A: Yes, simply copy `smart_parking.db` file to backup location.

**Q5: How do I restore data?**
A: Replace `smart_parking.db` with your backup copy.

---

### Admin Questions

**Q6: Can I change admin password?**
A: Not in UI. Requires direct database edit or delete and recreate.

**Q7: Can I add multiple admin accounts?**
A: Yes, using the `add_admin()` function (requires code modification).

**Q8: What's the maximum number of slots?**
A: No hard limit. Database can handle thousands.

**Q9: Can I export booking reports?**
A: Not in current version. Planned for future release.

**Q10: How do I see revenue?**
A: Sum up costs from completed bookings manually.

---

### User Questions

**Q11: Can I book for future dates?**
A: No, only immediate booking supported currently.

**Q12: Can I extend my parking?**
A: No need. Stay parked, duration auto-increases.

**Q13: What if I forget my password?**
A: Contact admin to reset (requires database access).

**Q14: Can I change my vehicle number?**
A: Update in booking form before booking. Registration vehicle is just default.

**Q15: Can I book multiple slots?**
A: No, only one active booking per user.

---

### Technical Questions

**Q16: Which database is used?**
A: SQLite3 (built-in with Python).

**Q17: Can I use MySQL/PostgreSQL?**
A: Requires code modification to change database adapter.

**Q18: Is it secure?**
A: Basic security. Passwords stored as plain text (improve for production).

**Q19: Can I customize the UI colors?**
A: Yes, edit color codes in UI files (hex color values).

**Q20: How do I change parking rate?**
A: Edit `utils/helpers.py` → `calculate_cost()` function.

---

## 📞 Support

### Getting Help

1. **Read documentation**:
   - README.md (overview)
   - QUICKSTART.md (quick guide)
   - This manual (detailed guide)

2. **Check code comments**:
   - All files well-documented
   - Functions have docstrings

3. **Review examples**:
   - Run populate_demo_data.py
   - Test all features

### Reporting Issues

If you find bugs:
1. Note exact error message
2. List steps to reproduce
3. Check troubleshooting section
4. Review code for issues

---

## 🎓 Tips for Success

### For Administrators:
1. ✅ Set up demo data before showing to users
2. ✅ Keep slot numbering organized
3. ✅ Monitor statistics regularly
4. ✅ Review bookings daily
5. ✅ Backup database weekly

### For Users:
1. ✅ Remember your slot number and floor
2. ✅ Checkout promptly to avoid high costs
3. ✅ Check duration before checkout
4. ✅ Keep vehicle info updated
5. ✅ Review booking history

---

## 📚 Additional Resources

- **README.md** - Project overview
- **QUICKSTART.md** - Quick start guide
- **PROJECT_SUMMARY.md** - Technical summary
- **ARCHITECTURE.md** - System design
- **CHANGELOG.md** - Version history

---

**Happy Parking! 🚗🅿️**

---

**User Manual Version: 1.0.0**
**Last Updated: November 2, 2025**
**© 2025 Smart Parking System**
