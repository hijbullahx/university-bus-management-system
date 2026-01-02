# IUBAT Bus Management System

A modern Django-based web application for managing university bus routes, schedules, and shuttle services. Designed for IUBAT, but easily adaptable for other institutions.

## Features

- **User Home Page**: View all bus and shuttle routes, with clear schedules and route details.
- **Shuttle Bus Support**: Special UI and schedule table for shuttle buses (no stopages, only timetable).
- **Custom Admin Panel**: Create, edit, and delete routes and shuttle routes with a user-friendly interface.
- **12-hour Time Format**: All times displayed in 12-hour format with AM/PM selection.
- **Dynamic Formsets**: Add/remove stopages and shuttle schedules with dropdowns and time pickers.
- **Responsive Design**: Mobile-friendly, modern yellow and green theme.
- **REST API Ready**: Includes Django REST Framework for future API integrations.

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/hijbullahx/university-bus-management-system.git
cd university-bus-management-system
```

### 2. Install Dependencies
```bash
pip install -r Requirements.txt
```

### 3. Database Setup
```bash
python manage.py migrate
```

### 4. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 5. Run the Server
```bash
python manage.py runserver
```

### 6. Access the App
- **User Home Page**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Admin Panel**: [http://127.0.0.1:8000/admin-panel/](http://127.0.0.1:8000/admin-panel/)

## Project Structure

```
Requirements.txt
bus_project/
    manage.py
    bus_management_project/
        settings.py
        urls.py
        ...
    buses/
        models.py
        forms.py
        forms_shuttle_schedule.py
        views.py
        views_admin_shuttle.py
        views_admin_shuttle_edit.py
        templates/
            bus_schedule_list.html
            route_stopages_detail.html
            buses/custom_admin/
                dashboard.html
                create_route.html
                edit_route.html
                create_shuttle_route.html
                edit_shuttle_route.html
                ...
```

## Key Technologies
- Django 4.2+
- Django REST Framework
- HTML5, CSS3 (custom theme)
- SQLite (default, can use PostgreSQL)

## Usage
- **Users**: View bus and shuttle schedules, route details.
- **Admins**: Login to admin panel, manage routes, stopages, and shuttle timetables.

## Customization
- Change theme colors in `bus_schedule_list.html` and `base.html`.
- Add/modify bus routes and schedules via the admin panel.
- Extend with REST API endpoints for mobile apps or integrations.

## Deployment
- Use Gunicorn and Whitenoise for production.
- Supports Heroku, Railway, or any cloud platform.

## License
MIT License

## Author
- [hijbullahx](https://github.com/hijbullahx)

---

For any issues or feature requests, please open an issue on GitHub.
