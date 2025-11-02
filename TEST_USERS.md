# Test User Credentials

## Admin Account
- **Username:** admin
- **Password:** admin123
- **Access:** Full admin dashboard with slot and booking management

---

## Test User Accounts

All test users have the password: **demo123** or **[username]123**

| Username | Password | Email | Phone | Vehicle Number |
|----------|----------|-------|-------|----------------|
| demo1 | demo123 | demo1@test.com | 9876543210 | MH12AB1234 |
| demo2 | demo123 | demo2@test.com | 9876543211 | KA01CD5678 |
| demo3 | demo123 | demo3@test.com | 9876543212 | TN09EF9012 |
| john | john123 | john@test.com | 9876543213 | DL07GH3456 |
| mary | mary123 | mary@test.com | 9876543214 | MH14IJ7890 |
| user1 | user123 | xyz@gmail.com | - | KA-05-SU1234 |
| user2 | user123 | exy@gmail.com | - | KA06-AB7896 |

---

## Quick Test Steps

### 1. Login as a User
```
http://localhost:5000
Username: demo1
Password: demo123
```

### 2. Book a Parking Slot
1. Click "Book Slot" from navigation
2. Select floor from dropdown (Floor 1 or Floor 2)
3. Click on any **green slot card**
4. **Vehicle number is pre-filled** with your saved vehicle (MH12AB1234)
5. Choose package (Hourly, Half Day, Full Day, Weekly, Monthly)
6. Select "Now" for immediate booking or "Schedule Later" for future
7. Click "Confirm Booking"

### 3. View Your Active Parking
- Dashboard shows current parking with duration and cost
- Click "Checkout" to end parking and calculate final cost

### 4. View Booking History
- Click "My Bookings" to see all past bookings
- Shows booking time, checkout time, duration, and cost

---

## Features Tested

✅ **Database Fixed:** Added missing package columns to bookings table
✅ **7 Test Users Added:** With different vehicle numbers
✅ **Saved Vehicle Numbers:** Auto-filled in booking form
✅ **Vehicle Selection:** Choose saved vehicle or enter new one
✅ **Package Selection:** 5 parking packages available
✅ **Date/Time Booking:** Book now or schedule for later
✅ **Cost Calculation:** Automatic based on duration and package

---

## Vehicle Number Quick Select

When you login as any test user:
- Your saved vehicle number appears in the booking form
- Dropdown shows: "MH12AB1234 (Saved)" or your vehicle
- Select "Enter New Vehicle Number" to type a different one
- Makes booking faster and easier!

---

## Troubleshooting

If booking still fails:
1. Check terminal output for error messages
2. Ensure you've selected a slot (green card should have blue border)
3. Verify vehicle number is filled
4. Try with "Now" option first before "Schedule Later"
5. Check that you don't already have an active booking

---

**All bugs fixed! Database updated! Test users ready! 🎉**
