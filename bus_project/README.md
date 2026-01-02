# 🚌 IUBAT Bus Management System

A complete production-ready Django-based bus tracking and management system for IUBAT (International University of Business Agriculture and Technology).

## 🎯 Features

### **4 Actor Roles System**

1. **👤 USER Role**
   - View live bus tracking on interactive Leaflet.js map
   - See real-time bus locations and routes
   - Receive system notifications
   - View bus schedules

2. **🚗 DRIVER Role**
   - Mobile-responsive dashboard
   - Start/Stop route tracking
   - Automatic GPS location posting every 10 seconds
   - Report issues (Breakdown, Traffic, Emergency, Accident)
   - View assigned bus and route information

3. **👨‍💼 ADMIN Role**
   - Comprehensive dashboard with statistics
   - Manage routes and schedules
   - View reports with Chart.js visualizations
   - Monitor live bus tracking
   - Manage issues and notifications
   - View on-time performance metrics

4. **🏛️ AUTHORITY Role**
   - Full system management access
   - All admin features plus oversight capabilities
   - System-wide configuration

## 🚀 Quick Start

### 1. Setup Environment

```bash
cd bus_project
python -m venv ../venv
source ../venv/Scripts/activate  # Windows
pip install -r Requirements.txt
```

### 2. Configure Database

```bash
python manage.py migrate
python manage.py populate_sample_data
python manage.py create_test_users
```

### 3. Run Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/buses/login/**

## 🔐 Test User Credentials

| Role      | Username  | Password     | Access                          |
|-----------|-----------|--------------|--------------------------------|
| USER      | testuser  | user123      | Bus tracking map               |
| DRIVER    | driver1   | driver123    | Driver dashboard + GPS         |
| DRIVER    | driver2   | driver123    | Driver dashboard + GPS         |
| ADMIN     | admin     | admin123     | Admin dashboard + management   |
| AUTHORITY | authority | authority123 | Full system access             |

## 🗺️ Key URLs

- **Login**: `/buses/login/`
- **User Map**: `/buses/map/`
- **Driver Dashboard**: `/buses/driver/`
- **Admin Dashboard**: `/buses/admin-dashboard/`
- **API Endpoints**: `/api/`

## 🎮 GPS Simulation

```bash
# Run simulation for testing
python manage.py simulate_bus_gps

# Stops automatically when real driver starts tracking
```

## 🚢 Production Deployment

### Deploy to Render/Railway

1. Set environment variables: `SECRET_KEY`, `DATABASE_URL`, `DEBUG=False`
2. Build Command: `./build.sh`
3. Start Command: `gunicorn bus_management_project.wsgi:application`

Pre-configured with WhiteNoise, Gunicorn, and PostgreSQL support.

## 🔧 Technical Stack

- Django 4.2.23, Python 3.9+
- Leaflet.js for maps
- Chart.js for reports
- Django REST Framework for API
- IUBAT Green (#2D5016) & Yellow (#FFD700) branding

---

**© 2026 IUBAT University - Built with ❤️**
