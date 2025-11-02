# 🏗️ Project Architecture - Smart Parking System

## 📂 Complete Directory Structure

```
smart parking system/
│
├── 📁 database/                    # Database layer
│   ├── __init__.py                # Package initializer
│   ├── db_manager.py              # Database operations (150 lines)
│   └── smart_parking.db           # SQLite database (auto-generated)
│
├── 📁 modules/                     # Business logic layer
│   ├── __init__.py                # Package initializer
│   ├── authentication.py          # Login & registration (100 lines)
│   ├── slot_manager.py            # Slot CRUD operations (150 lines)
│   └── booking_manager.py         # Booking operations (180 lines)
│
├── 📁 ui/                          # Presentation layer
│   ├── __init__.py                # Package initializer
│   ├── login_window.py            # Login & registration UI (350 lines)
│   ├── admin_dashboard.py         # Admin interface (550 lines)
│   └── user_dashboard.py          # User interface (500 lines)
│
├── 📁 utils/                       # Helper utilities
│   ├── __init__.py                # Package initializer
│   ├── validators.py              # Input validation (50 lines)
│   └── helpers.py                 # Helper functions (40 lines)
│
├── 📄 main.py                      # Application entry point (30 lines)
├── 📄 populate_demo_data.py        # Demo data generator (100 lines)
│
├── 📘 README.md                    # Main documentation
├── 📗 QUICKSTART.md                # Quick start guide
├── 📙 PROJECT_SUMMARY.md           # Project summary
├── 📕 CHANGELOG.md                 # Version history
├── 📔 ARCHITECTURE.md              # This file
└── 📄 requirements.txt             # Dependencies (none!)
```

---

## 🏛️ System Architecture

### Three-Tier Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  ┌──────────────┐  ┌───────────────┐  ┌───────────────┐   │
│  │ Login Window │  │ Admin Dash    │  │ User Dash     │   │
│  │  - Login     │  │ - Stats       │  │ - Book Slot   │   │
│  │  - Register  │  │ - Manage Slots│  │ - My Bookings │   │
│  │  - Validate  │  │ - View Book   │  │ - Checkout    │   │
│  └──────────────┘  └───────────────┘  └───────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                     BUSINESS LOGIC LAYER                     │
│  ┌──────────────┐  ┌───────────────┐  ┌───────────────┐   │
│  │Authentication│  │ Slot Manager  │  │Booking Manager│   │
│  │ - Login      │  │ - Add Slot    │  │ - Book        │   │
│  │ - Register   │  │ - Update      │  │ - Cancel      │   │
│  │ - Validate   │  │ - Delete      │  │ - View        │   │
│  └──────────────┘  └───────────────┘  └───────────────┘   │
│                                                              │
│  ┌──────────────┐  ┌───────────────┐                       │
│  │  Validators  │  │    Helpers    │                       │
│  │ - Email      │  │ - DateTime    │                       │
│  │ - Phone      │  │ - Cost Calc   │                       │
│  │ - Vehicle    │  │ - Duration    │                       │
│  └──────────────┘  └───────────────┘                       │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                       DATA ACCESS LAYER                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Database Manager                         │  │
│  │  - Connect/Disconnect                                 │  │
│  │  - Execute queries                                    │  │
│  │  - Fetch results                                      │  │
│  │  - Transaction management                             │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                      DATABASE LAYER                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              SQLite Database                         │   │
│  │                                                       │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │   │
│  │  │  admin  │ │  users  │ │  slots  │ │bookings │   │   │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘   │   │
│  │       │           │           │           │          │   │
│  │       └───────────┴───────────┴───────────┘          │   │
│  │              (Foreign Key Relationships)             │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Diagrams

### User Booking Flow

```
┌──────────┐
│   User   │
└────┬─────┘
     │ 1. Login
     ↓
┌────────────────┐
│ Login Window   │
└────┬───────────┘
     │ 2. Validate credentials
     ↓
┌────────────────┐
│Authentication  │ → Database query
└────┬───────────┘
     │ 3. Success → Open User Dashboard
     ↓
┌────────────────┐
│ User Dashboard │
└────┬───────────┘
     │ 4. Select slot
     ↓
┌────────────────┐
│Available Slots │ ← Slot Manager
└────┬───────────┘
     │ 5. Book slot
     ↓
┌────────────────┐
│Booking Manager │ → Create booking record
└────┬───────────┘   → Update slot status
     │
     ↓
┌────────────────┐
│   Database     │
└────────────────┘
```

### Admin Slot Management Flow

```
┌──────────┐
│  Admin   │
└────┬─────┘
     │ 1. Login
     ↓
┌────────────────┐
│ Login Window   │
└────┬───────────┘
     │ 2. Validate credentials
     ↓
┌────────────────┐
│Authentication  │ → Database query
└────┬───────────┘
     │ 3. Success → Open Admin Dashboard
     ↓
┌────────────────┐
│Admin Dashboard │
└────┬───────────┘
     │ 4. Add slot
     ↓
┌────────────────┐
│ Slot Manager   │ → Validate slot number
└────┬───────────┘ → Check duplicates
     │            → Insert record
     ↓
┌────────────────┐
│   Database     │
└────────────────┘
     │
     ↓ 5. Refresh statistics
┌────────────────┐
│Admin Dashboard │ ← Slot statistics
└────────────────┘ ← Booking statistics
```

---

## 🗄️ Database Schema

### ER Diagram

```
┌─────────────────┐
│     admin       │
├─────────────────┤
│ * id (PK)       │
│   username      │
│   password      │
│   email         │
│   created_at    │
└─────────────────┘


┌─────────────────┐           ┌─────────────────┐
│     users       │           │     slots       │
├─────────────────┤           ├─────────────────┤
│ * id (PK)       │           │ * id (PK)       │
│   username      │           │   slot_number   │
│   password      │           │   slot_type     │
│   email         │           │   status        │
│   phone         │           │   floor         │
│   vehicle_no    │           │   created_at    │
│   created_at    │           └─────────────────┘
└─────────────────┘                    │
        │                              │
        │                              │
        │         ┌─────────────────┐  │
        │         │   bookings      │  │
        │         ├─────────────────┤  │
        │         │ * id (PK)       │  │
        └────────→│   user_id (FK)  │  │
                  │   slot_id (FK)  │←─┘
                  │   vehicle_no    │
                  │   booking_time  │
                  │   checkout_time │
                  │   status        │
                  └─────────────────┘

Legend:
* = Primary Key
→ = Foreign Key relationship
PK = Primary Key
FK = Foreign Key
```

---

## 🧩 Component Interaction

### Module Dependencies

```
main.py
  │
  └─→ ui/login_window.py
        │
        ├─→ modules/authentication.py
        │     └─→ database/db_manager.py
        │     └─→ utils/validators.py
        │
        ├─→ ui/admin_dashboard.py
        │     ├─→ modules/slot_manager.py
        │     │     └─→ database/db_manager.py
        │     │     └─→ utils/validators.py
        │     │
        │     └─→ modules/booking_manager.py
        │           └─→ database/db_manager.py
        │           └─→ utils/helpers.py
        │
        └─→ ui/user_dashboard.py
              ├─→ modules/slot_manager.py
              │     └─→ database/db_manager.py
              │     └─→ utils/validators.py
              │
              └─→ modules/booking_manager.py
                    └─→ database/db_manager.py
                    └─→ utils/helpers.py
```

---

## 🎯 Design Patterns Used

### 1. **Singleton Pattern**
- `DatabaseManager` - Single database connection

### 2. **Model-View-Controller (MVC)**
- **Model**: `database/`, `modules/`
- **View**: `ui/`
- **Controller**: Business logic in `modules/`

### 3. **Repository Pattern**
- `DatabaseManager` acts as repository for data access

### 4. **Validator Pattern**
- Separate validation logic in `utils/validators.py`

### 5. **Helper/Utility Pattern**
- Common functions in `utils/helpers.py`

---

## 🔐 Security Architecture

```
User Input
    │
    ↓
┌─────────────────┐
│   Validators    │ ← Email, Phone, Vehicle, etc.
└────┬────────────┘
     │ Valid?
     ↓ Yes
┌─────────────────┐
│  Sanitization   │ ← Strip, Upper case, etc.
└────┬────────────┘
     │
     ↓
┌─────────────────┐
│ SQL Parameters  │ ← Prevent SQL injection
└────┬────────────┘
     │
     ↓
┌─────────────────┐
│   Database      │
└─────────────────┘
```

---

## 📊 State Management

### Application States

```
┌────────────┐
│   Start    │
└─────┬──────┘
      │
      ↓
┌────────────┐
│Login Screen│←─────────────┐
└─────┬──────┘              │
      │                     │
      ├─→ Admin ──→ Admin Dashboard
      │                     │
      └─→ User  ──→ User Dashboard
                            │
                       Logout
                            │
                            ↓
                    ┌────────────┐
                    │   Close    │
                    └────────────┘
```

### Slot Status States

```
┌──────────────┐
│  Available   │
└──────┬───────┘
       │ User books slot
       ↓
┌──────────────┐
│   Occupied   │
└──────┬───────┘
       │ User checks out
       ↓
┌──────────────┐
│  Available   │
└──────────────┘
```

### Booking Status States

```
┌──────────────┐
│    Active    │ ← New booking
└──────┬───────┘
       │ User cancels/checks out
       ↓
┌──────────────┐
│  Completed   │ ← Historical record
└──────────────┘
```

---

## 🚀 Performance Considerations

### Database Optimization
- Indexed primary keys
- Foreign key constraints for referential integrity
- Efficient queries with WHERE clauses
- No N+1 query problems

### UI Optimization
- Lazy loading of data
- Efficient tree view rendering
- Minimal redraws
- Event-driven updates

### Memory Management
- Connection pooling (single connection)
- Proper resource cleanup
- No memory leaks
- Efficient data structures

---

## 📏 Coding Standards

### Naming Conventions
- **Classes**: `PascalCase` (e.g., `DatabaseManager`)
- **Functions**: `snake_case` (e.g., `get_user_bookings`)
- **Variables**: `snake_case` (e.g., `user_id`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_RATE`)
- **Private**: `_leading_underscore` (e.g., `_internal_method`)

### File Structure
- Each module in separate file
- Related functions grouped together
- Clear separation of concerns
- Docstrings for all classes and functions

### Code Organization
```python
"""
Module docstring
"""

# Imports (standard library first)
import tkinter as tk
from datetime import datetime

# Imports (local modules)
from database.db_manager import DatabaseManager

# Class definition
class ClassName:
    """Class docstring"""
    
    def __init__(self):
        """Initialize"""
        pass
    
    def public_method(self):
        """Method docstring"""
        pass
```

---

## 🧪 Testing Strategy

### Unit Testing (Manual)
- Each module function tested independently
- Edge cases validated
- Input validation verified

### Integration Testing (Manual)
- Database operations with UI
- Module interactions
- Complete workflows

### User Acceptance Testing
- Admin workflows
- User workflows
- Error scenarios

---

## 📦 Deployment Architecture

```
┌─────────────────────────────────────┐
│     Smart Parking System            │
│                                     │
│  ┌──────────────────────────────┐  │
│  │      Python Runtime          │  │
│  │      (Python 3.7+)           │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │     Application Code         │  │
│  │  (All Python modules)        │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │    SQLite Database           │  │
│  │  (smart_parking.db)          │  │
│  └──────────────────────────────┘  │
│                                     │
└─────────────────────────────────────┘
         │
         ↓
    User's Computer
    (Windows/Mac/Linux)
```

---

## 🔮 Scalability Considerations

### Current Limitations
- Single database file (SQLite)
- Single-user GUI application
- Local deployment only

### Future Scalability Options
1. **Database**: Migrate to PostgreSQL/MySQL for multi-user
2. **Architecture**: Convert to client-server model
3. **Interface**: Add web interface (Flask/Django)
4. **API**: RESTful API for mobile apps
5. **Cloud**: Deploy to cloud platforms
6. **Caching**: Redis for session management
7. **Load Balancing**: For high traffic

---

## 📚 Technology Stack Details

### Core Technologies
```
┌──────────────────────────────────────────┐
│         Python 3.7+                      │
│  ┌────────────────────────────────────┐ │
│  │  Standard Library Modules:         │ │
│  │  - tkinter (GUI)                   │ │
│  │  - sqlite3 (Database)              │ │
│  │  - datetime (Time handling)        │ │
│  │  - re (Regex validation)           │ │
│  │  - os (File operations)            │ │
│  └────────────────────────────────────┘ │
└──────────────────────────────────────────┘
```

### No External Dependencies!
- Self-contained application
- Easy deployment
- No dependency conflicts
- Minimal system requirements

---

**Architecture Version: 1.0.0**
**Last Updated: November 2, 2025**
