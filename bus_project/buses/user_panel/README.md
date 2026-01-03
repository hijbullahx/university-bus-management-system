# User Panel Module

## Overview
The user panel module contains all public-facing functionality for bus tracking and schedule viewing. This module has been separated from the main buses app to improve code organization and maintainability.

## Directory Structure
```
user_panel/
├── __init__.py           # Module initialization
├── views.py              # User panel view functions
├── urls.py               # URL routing for user panel
└── templates/
    └── user_panel/
        ├── user_map.html          # Live bus tracking map
        ├── home.html              # Home page with role-based tabs
        └── bus_schedule_list.html # Bus schedules display
```

## Features

### 1. Live Bus Tracking (`user_map.html`)
- **Full-screen interactive map** with OpenStreetMap tiles
- **Real-time bus tracking** with automatic 10-second updates
- **Bus-shaped moving icons** with distinct styling:
  - Green icons for live GPS tracking
  - Orange icons for simulation mode
- **Enhanced popup information** including:
  - Bus ID and Bus Number
  - Route Name
  - **ETA to next stop** (calculated in real-time)
  - **Next stop name**
  - Current speed
  - Distance to next stop
  - Last update timestamp
- **"Follow" button functionality**:
  - One-click to follow any bus
  - Map auto-centers every 3 seconds
  - Visual feedback with button state
  - Easy stop following
- **Route selection dropdown**:
  - Filter buses by specific route
  - "All Routes" option
  - Real-time filtering without page reload
- **Collapsible sidebar** with:
  - Active notifications display
  - Quick route access buttons
  - Space-saving toggle button
- **Live statistics bar**:
  - Active bus count
  - Total routes
  - System status indicator
- Interactive markers with hover effects
- Responsive design for all devices

**URL**: `/buses/user/map/` or `/buses/user/`

### 2. Bus Schedules (`bus_schedule_list.html`)
- Display all bus routes and their schedules
- Separate views for regular and shuttle routes
- Filter by schedule type (Regular/Friday/Holiday)
- Link to detailed stopage information
- Responsive design

**URL**: `/buses/user/schedules/`

### 3. Home Page (`home.html`)
- Unified interface with role-based navigation tabs
- Dashboard statistics
- Embedded map view
- Tab-based navigation for:
  - Home dashboard
  - Live tracking
  - Driver dashboard (if driver)
  - Admin dashboard (if admin/authority)
  - Schedule viewing

**URL**: `/buses/user/home/` (requires authentication)

## URL Configuration

### New URLs (User Panel)
```python
/buses/user/              # Main map view
/buses/user/map/          # Same as above
/buses/user/schedules/    # Bus schedules
/buses/user/home/         # Home page (auth required)
/buses/user/simulation-status/  # Check simulation status
```

### Legacy URLs (Backward Compatibility)
The following URLs are maintained for backward compatibility:
```python
/buses/map/               # Redirects to old view
/buses/schedules/         # Redirects to old view
/buses/home/              # Redirects to old view
```

## View Functions

### `user_map_view(request)`
Main map view for tracking live bus locations.
- **Authentication**: Not required
- **Template**: `user_panel/user_map.html`
- **Context**:
  - `notifications`: Active notifications
  - `routes`: All bus routes
  - `page_title`: Page title

### `bus_schedule_list(request)`
Display bus schedules with filtering by type.
- **Authentication**: Not required
- **Template**: `user_panel/bus_schedule_list.html`
- **Context**:
  - `routes`: Bus routes with active schedules
  - `current_time`: Current time in Dhaka timezone
  - `active_schedule_type_display`: Active schedule type name
  - `active_schedule_type_raw`: Active schedule type code

### `home_view(request)`
Unified home page with role-based content.
- **Authentication**: Required
- **Template**: `user_panel/home.html`
- **Context**:
  - `page_title`: Page title
  - `total_buses`: Total number of buses
  - `total_routes`: Total number of routes
  - `total_schedules`: Total active schedules
  - `active_buses`: Currently active buses

### `simulation_status(request)`
Check if system is in simulation mode.
- **Authentication**: Not required
- **Template**: `user_panel/simulation_status.html`
- **Context**:
  - `real_buses_count`: Number of real buses
  - `simulated_buses_count`: Number of simulated buses
  - `simulation_mode`: Boolean indicating if in simulation mode

## Integration with Main App

### URL Routing
The user panel is included in the main buses app URLs:
```python
# In buses/urls.py
path('user/', include('buses.user_panel.urls', namespace='user_panel')),
```

### Template References
Templates can reference user panel URLs using:
```django
{% url 'buses:user_panel:map' %}
{% url 'buses:user_panel:schedules' %}
{% url 'buses:user_panel:home' %}
```

### API Integration
The user panel uses the main API endpoints:
- `/api/map-data/` - For live bus location data
- `/api/routes/` - For route information
- `/api/notifications/` - For notification data

## Dependencies

### Python Packages
- Django (views, templates, URLs)
- pytz (timezone handling)

### Frontend Libraries
- Leaflet.js 1.9.4 (map display)
- Chart.js (statistics visualization)
- OpenStreetMap (map tiles)

### Models Used
From `buses.models`:
- `BusRoute` - Bus route information
- `BusLocation` - Live GPS locations
- `BusSchedule` - Schedule data
- `Notification` - System notifications
- `GlobalSettings` - System configuration

## Customization

### Styling
The templates use inline CSS with IUBAT branding:
- Primary color: `#2D5016` (IUBAT Green)
- Accent color: `#FFD700` (IUBAT Yellow)
- Light green: `#4A7C2A`

### Map Configuration
Default map center: IUBAT University (23.8859, 90.3971)
Default zoom: 13
Refresh interval: 10 seconds

### Responsive Design
All templates include mobile-responsive breakpoints at 768px.

## Future Enhancements
- [ ] User authentication for personalized tracking
- [ ] Favorite routes feature
- [ ] Push notifications for bus arrivals
- [ ] Estimated time of arrival (ETA) calculations
- [ ] Route planning and suggestions
- [ ] Offline mode support
- [ ] Progressive Web App (PWA) features

## Testing
To test the user panel:
1. Start the development server: `python manage.py runserver`
2. Navigate to: `http://localhost:8000/buses/user/`
3. Verify map displays correctly
4. Check that bus markers appear
5. Test schedule viewing
6. Test authentication for home page

## Maintenance Notes
- Keep templates in sync with main app models
- Update API endpoints if data structure changes
- Maintain backward compatibility with legacy URLs
- Test responsive design on mobile devices
- Monitor JavaScript console for errors
