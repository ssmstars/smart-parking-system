# Smart Parking System - Web Application

A modern web-based parking management system built with Flask and Bootstrap.

## Features

### For Users:
- 🚗 Easy slot booking with visual selection
- 📍 Floor-based filtering
- 💰 Multiple parking packages (Hourly, Half Day, Full Day, Weekly, Monthly)
- 📊 Real-time booking status
- 💳 Automated cost calculation
- 📜 Booking history

### For Admins:
- 👥 User management
- 🅿️ Slot management (Add/Delete slots)
- 📈 Dashboard with statistics
- 📋 View all bookings

## Quick Start

### 1. Install Dependencies
```bash
pip install Flask
```

### 2. Run the Application
```bash
python app.py
```

### 3. Access the System
Open your browser and go to: **http://localhost:5000**

### 4. Login Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**User Account:**
- Register a new account or use demo data

## Parking Packages

| Package | Duration | Cost |
|---------|----------|------|
| Hourly | 1 hour | ₹50/hour |
| Half Day | 6 hours | ₹250 |
| Full Day | 24 hours | ₹400 |
| Weekly | 7 days | ₹2,500 |
| Monthly | 30 days | ₹8,000 |

## How to Book a Slot

1. **Login** to your account
2. Click **"Book Slot"** from the menu
3. **Select a floor** from the dropdown menu
4. **Click on an available slot** (green cards)
5. **Enter your vehicle number**
6. **Choose a parking package**
7. Click **"Confirm Booking"**

## Project Structure

```
smart parking system/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── smart_parking.db      # SQLite database
├── database/             # Database manager
├── modules/              # Business logic
├── templates/            # HTML templates
└── utils/               # Helper utilities
```

## Technologies Used

- **Backend:** Python 3.7+, Flask 3.0
- **Frontend:** HTML5, Bootstrap 5.3, JavaScript
- **Database:** SQLite3
- **Icons:** Bootstrap Icons

## Demo Data

To populate demo parking slots:
```bash
python populate_demo_data.py
```

---

**Developed with ❤️ for efficient parking management**
