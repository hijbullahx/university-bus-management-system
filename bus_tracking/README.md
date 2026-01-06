# 🚌 UBus - Real-Time Bus Tracking & Management System

A production-ready Django + Bootstrap + Streamlit application for university bus tracking and fleet management.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Features

### 🗺️ Real-Time Tracking
- Live bus locations on interactive map (Leaflet.js)
- GPS-based ETA calculations with Haversine formula
- 5-second location update intervals
- Route visualization with stop markers

### 👥 Multi-Role Authentication
- **Students/Users**: View schedules, track buses, submit feedback
- **Drivers**: Update locations, report issues, view assignments
- **Administrators**: Manage users, buses, routes, and schedules
- **Authority**: Access analytics, reports, and system oversight

### 📅 Schedule Management
- Route creation with ordered stops
- Flexible scheduling (daily, weekday, weekend)
- Schedule exceptions for holidays
- Stop-level ETA tracking

### ⚠️ Issue Reporting
- Driver issue submission with attachments
- Issue categories: mechanical, traffic, emergency, accident, weather
- Priority levels and status tracking
- Admin resolution workflow

### 🔔 Notifications
- Targeted notifications (all users, drivers, specific routes)
- Priority levels: info, warning, danger, success
- Expiration dates for time-sensitive alerts
- Real-time notification polling

### 📊 Analytics & Reports
- Route popularity analysis
- On-time performance metrics
- Driver incident logs
- User feedback summary
- PDF export functionality

### 📈 Streamlit Dashboard
- Interactive analytics visualizations
- System overview with key metrics
- Route comparison charts
- Trend analysis

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip (Python package manager)

### Backend Setup

```bash
# Navigate to backend directory
cd bus_tracking/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations accounts buses schedules issues notifications reports
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Streamlit App Setup

```bash
# Navigate to streamlit directory
cd bus_tracking/streamlit_app

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py
```

## 📁 Project Structure

```
bus_tracking/
├── backend/
│   ├── core/                 # Django settings & URLs
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   └── asgi.py
│   ├── accounts/             # User authentication & profiles
│   │   ├── models.py         # User, DriverProfile
│   │   ├── views.py
│   │   ├── decorators.py     # Role-based access control
│   │   └── templates/
│   ├── buses/                # Bus management & tracking
│   │   ├── models.py         # Bus, BusLocation, ETACalculation
│   │   ├── views.py
│   │   ├── api_views.py      # REST API endpoints
│   │   └── templates/
│   ├── schedules/            # Routes & scheduling
│   │   ├── models.py         # Route, Stop, Schedule
│   │   ├── views.py
│   │   ├── api_views.py
│   │   └── templates/
│   ├── issues/               # Issue reporting system
│   │   ├── models.py         # Issue, IssueComment
│   │   ├── views.py
│   │   ├── api_views.py
│   │   └── templates/
│   ├── notifications/        # Notification system
│   │   ├── models.py         # Notification, UserNotification
│   │   ├── views.py
│   │   ├── api_views.py
│   │   └── templates/
│   ├── reports/              # Analytics & reporting
│   │   ├── models.py         # TripLog, UserFeedback, RouteAnalytics
│   │   ├── views.py
│   │   ├── api_views.py
│   │   └── templates/
│   ├── templates/            # Base templates
│   │   └── base.html
│   ├── manage.py
│   └── requirements.txt
└── streamlit_app/
    ├── app.py                # Streamlit analytics dashboard
    └── requirements.txt
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

### Key Settings (core/settings.py)

| Setting | Default | Description |
|---------|---------|-------------|
| `GPS_UPDATE_INTERVAL` | 5 | Seconds between GPS updates |
| `ETA_CALCULATION_BUFFER` | 1.2 | Buffer multiplier for ETA |
| `DEFAULT_BUS_SPEED` | 25 | Default speed in km/h |

## 📱 API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `POST /api/auth/register/` - User registration

### Buses
- `GET /api/buses/` - List all buses
- `GET /api/buses/{id}/location/` - Get bus location
- `POST /api/buses/location/update/` - Update bus location
- `GET /api/buses/live/` - Get all live bus locations

### Schedules
- `GET /api/schedules/routes/` - List routes
- `GET /api/schedules/routes/{id}/stops/` - Route stops
- `GET /api/schedules/` - List schedules

### Issues
- `GET /api/issues/` - List issues
- `POST /api/issues/` - Create issue
- `PUT /api/issues/{id}/` - Update issue

### Notifications
- `GET /api/notifications/` - List notifications
- `GET /api/notifications/unread/` - Unread notifications
- `POST /api/notifications/{id}/read/` - Mark as read

### Reports
- `GET /api/reports/analytics/` - Route analytics
- `GET /api/reports/performance/` - Performance metrics
- `GET /api/reports/export/` - Export data

## 🗄️ Database Models

### User Roles
- `student` - Student user
- `faculty` - Faculty member
- `staff` - Staff member
- `driver` - Bus driver
- `admin` - System administrator
- `authority` - Authority/oversight

### ETA Calculation
Uses Haversine formula for accurate distance calculations:

```python
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in km
    # ... Haversine implementation
    return distance_km
```

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG=False`
2. Generate secure `SECRET_KEY`
3. Configure production database (PostgreSQL recommended)
4. Set up static file serving (WhiteNoise)
5. Configure HTTPS
6. Set `ALLOWED_HOSTS`

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Streamlit Cloud
1. Push `streamlit_app/` to GitHub
2. Connect to Streamlit Cloud
3. Deploy from repository

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📞 Support

For support, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ for university transportation management**
