# 🚌 IUBAT Bus Management System - Complete Guide

A comprehensive, production-ready Django application for managing IUBAT university bus operations with real-time GPS tracking, driver management, and administrative dashboards.

## 🎯 Key Features

### 👥 User Role Features
- **Live Bus Tracking Map**: Interactive Leaflet.js map showing real-time bus locations
- **Simulation Mode**: Automatic simulation when no real buses are active
- **Route Information**: View all bus routes and schedules
- **Notifications**: Real-time alerts and announcements

### 🚗 Driver Role Features
- **Mobile-Responsive Dashboard**: Optimized for mobile devices
- **GPS Tracking**: Automatic location updates every 10 seconds using browser Geolocation API
- **Start/End Route**: Simple interface to begin and end route sessions
- **Issue Reporting**: Report breakdowns, traffic, emergencies, etc.

### 👨‍💼 Admin/Authority Role Features
- **Comprehensive Dashboard**: Overview of all system metrics
- **Live Tracking**: Monitor all active buses in real-time
- **Reports & Analytics**: Chart.js visualizations for performance metrics
- **Issue Management**: Track and resolve reported issues
- **Notification Management**: Create system-wide announcements

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.9+
- PostgreSQL
- Virtual environment

### Installation Steps

1. **Navigate to project directory**
```bash
cd d:/Projects/IUBAT_Bus/bus_project
```

2. **Virtual environment is already created at project root**
```bash
# Activate it
source ../venv/Scripts/activate  # Windows Git Bash
# or
..\venv\Scripts\activate  # Windows CMD
```

3. **Install dependencies** (already done)
```bash
pip install -r Requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser and user profiles**
```bash
python manage.py createsuperuser
# Then create UserProfile for roles via Django admin
```

7. **Run the server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the live map!

## 🗺️ URL Structure

- `/` - User map view (public, live bus tracking)
- `/schedules/` - Bus schedule list
- `/driver/` - Driver dashboard
- `/driver/tracking/` - Active GPS tracking
- `/admin-dashboard/` - Admin overview
- `/admin-dashboard/reports/` - Analytics with Chart.js
- `/admin-dashboard/live-tracking/` - Admin live tracking
- `/admin/` - Django admin panel
- `/api/map-data/` - API endpoint for map
- `/api/bus-locations/` - Bus location API

## 🎮 GPS Simulation System

### How It Works

The GPS simulation creates realistic bus movements when no real drivers are active:

1. **Automatic Detection**: Checks every update cycle for real drivers
2. **Path Generation**: Creates routes based on stopage data
3. **Linear Interpolation**: Smooth movement between waypoints
4. **Random Variations**: Adds realistic GPS noise
5. **Auto-Pause**: Stops when real driver detected

### Running Simulation

```bash
# Basic simulation (all buses, 10s interval)
python manage.py simulate_bus_gps

# Specific buses only
python manage.py simulate_bus_gps --buses 1 2 3

# Faster updates (5 seconds)
python manage.py simulate_bus_gps --interval 5

# Time-limited (5 minutes)
python manage.py simulate_bus_gps --duration 300

# Faster buses (40 km/h)
python manage.py simulate_bus_gps --speed 40
```

### Simulation Algorithm

```python
# Pseudocode for simulation
for each bus:
    create_circular_path_from_stopages()
    while simulation_active:
        if real_driver_detected:
            pause_simulation()
        else:
            calculate_new_position()
            add_random_noise()
            post_to_database()
            sleep(interval)
```

## 🏗️ System Architecture

### Database Models

**BusRoute** - Bus routes with stopages
- bus_number, route, is_shuttle, notes

**BusLocation** - Real-time GPS tracking
- bus, driver, lat, lng, timestamp, is_simulated

**IssueReport** - Driver problem reports
- bus, driver, issue_type, description, status

**Notification** - System announcements
- title, message, type, priority

**UserProfile** - Role management
- user, role (USER/DRIVER/ADMIN/AUTHORITY), assigned_bus

**DriverRouteSession** - Track sessions
- driver, bus, started_at, ended_at, distance

### API Architecture

**REST Framework Endpoints:**
- ViewSets for CRUD operations
- Custom actions for specific functionality
- Session-based authentication
- Role-based permissions

**Key API Views:**
- `BusLocationViewSet` - GPS location CRUD
- `bus_map_data()` - Optimized map endpoint
- `DriverRouteSessionViewSet` - Session management

## 🎨 Branding & Theme

**IUBAT Colors:**
- Primary Green: `#2D5016`
- Yellow: `#FFD700`
- Light Green: `#4A7C2A`

**UI Framework:**
- Custom CSS with CSS Grid and Flexbox
- Responsive design for mobile
- Leaflet.js for maps
- Chart.js for analytics

## 🌐 Deployment Guide

### For Render.com

1. **Create Web Service**
   - Repository: Connect your GitHub repo
   - Build Command: `./build.sh`
   - Start Command: `gunicorn bus_management_project.wsgi:application`

2. **Environment Variables**
```
SECRET_KEY=<generate-random-string>
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
DATABASE_URL=<provided-by-render>
```

3. **Create PostgreSQL Database**
   - Add PostgreSQL service in Render
   - Copy DATABASE_URL to environment

4. **Deploy**
   - Push to GitHub
   - Render auto-deploys

### For Railway.app

1. **New Project from GitHub**
   - Select repository
   - Add PostgreSQL plugin

2. **Environment Variables**
```
SECRET_KEY=<random-string>
DEBUG=False
```

3. **Deploy**
   - Automatic on git push
   - Railway handles DATABASE_URL

## 📊 API Documentation

### Public Endpoints

**GET /api/map-data/**
```json
{
  "buses": [
    {
      "bus_id": 1,
      "bus_number": "Bus 1",
      "route": "Main Campus",
      "latitude": 23.8859,
      "longitude": 90.3971,
      "speed": 30.5,
      "is_simulated": false,
      "timestamp": "2026-01-02T10:30:00Z"
    }
  ],
  "total_active": 1
}
```

### Authenticated Endpoints

**POST /api/bus-locations/** (Drivers)
```json
{
  "bus": 1,
  "latitude": 23.8859,
  "longitude": 90.3971,
  "speed": 30.5,
  "is_active": true
}
```

**POST /api/issues/** (Drivers)
```json
{
  "bus": 1,
  "issue_type": "TRAFFIC",
  "description": "Heavy congestion",
  "location_lat": 23.8859,
  "location_lng": 90.3971
}
```

**POST /api/driver-sessions/start_route/**
```json
{
  "bus_id": 1
}
```

## 🔐 Security Features

- Environment-based configuration
- CSRF protection
- Secure sessions (HTTPS in production)
- Role-based access control
- SQL injection protection
- XSS protection
- Secure password hashing

## 🧪 Testing

```bash
# Run all tests
python manage.py test buses

# Check for issues
python manage.py check

# Check deployment readiness
python manage.py check --deploy
```

## 📁 Project Structure

```
IUBAT_Bus/
├── venv/                      # Virtual environment (root)
├── bus_project/               # Django project
│   ├── bus_management_project/
│   │   ├── settings.py       # Environment-aware config
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── buses/
│   │   ├── models.py         # All database models
│   │   ├── views_user_map.py # User role views
│   │   ├── views_driver.py   # Driver role views
│   │   ├── views_admin_dashboard.py  # Admin views
│   │   ├── api_views.py      # REST API
│   │   ├── serializers.py    # DRF serializers
│   │   ├── templates/buses/
│   │   │   ├── user_map.html
│   │   │   ├── driver_tracking.html
│   │   │   └── admin_reports.html
│   │   ├── management/commands/
│   │   │   └── simulate_bus_gps.py
│   │   └── ...
│   ├── .env.example
│   ├── Requirements.txt
│   ├── Procfile
│   ├── build.sh
│   └── manage.py
└── .gitignore
```

## 🎓 User Roles Explained

### 1. User (Public)
- **No login required**
- Can view live map
- Can see schedules
- Can receive notifications

### 2. Driver
- **Requires login**
- Assigned to specific bus
- Can start/end routes
- GPS tracking active
- Can report issues

### 3. Admin
- **Requires login + admin role**
- Full system access
- Manage routes/schedules
- View all analytics
- Resolve issues

### 4. Authority
- **Same as Admin**
- Oversight role
- Additional permissions can be added

## 🚦 Workflow Example

### Driver Daily Flow:
1. Login to system
2. Navigate to Driver Dashboard
3. Click "Start Route"
4. Select assigned bus
5. System begins GPS tracking every 10s
6. Drive route (locations auto-posted)
7. Report any issues if needed
8. Click "End Route" when done
9. System logs session metrics

### Admin Monitoring:
1. Login to admin dashboard
2. View live tracking map
3. Monitor active buses
4. Check pending issues
5. View analytics reports
6. Create notifications if needed

## 🔧 Common Commands

```bash
# Development
python manage.py runserver

# Database
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Production
python manage.py collectstatic
gunicorn bus_management_project.wsgi:application

# Testing
python manage.py test
python manage.py check --deploy

# Simulation
python manage.py simulate_bus_gps
```

## 📞 Support & Maintenance

### Regular Maintenance:
- Clear old location data (older than 7 days)
- Review pending issues weekly
- Update bus schedules as needed
- Monitor simulation vs real ratio

### Database Cleanup:
```python
# In Django shell
from buses.models import BusLocation
from datetime import timedelta
from django.utils import timezone

old_date = timezone.now() - timedelta(days=7)
BusLocation.objects.filter(timestamp__lt=old_date).delete()
```

## 🎯 Future Enhancements

- Real-time WebSocket updates
- Push notifications for mobile
- Historical route playback
- Passenger capacity tracking
- ETA calculations
- Multi-language support
- SMS alerts for delays

## 📝 License & Credits

Developed for IUBAT (International University of Business Agriculture and Technology)

**Technologies Used:**
- Django 4.2
- Django REST Framework
- PostgreSQL
- Leaflet.js
- Chart.js
- WhiteNoise
- Gunicorn

---

**For deployment support or questions, refer to the documentation or contact the development team.**
