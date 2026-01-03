"""
User Panel Views - Public-facing map interface for users to track buses
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from buses.models import BusRoute, BusLocation, Notification, BusSchedule, GlobalSettings
from django.utils import timezone
from datetime import timedelta
from django.db.models import Prefetch
import pytz


def user_map_view(request):
    """
    Main map view for users to see live bus locations
    Shows Leaflet.js map with bus markers
    """
    # Get active notifications
    notifications = Notification.objects.filter(
        is_active=True
    ).order_by('-priority', '-created_at')[:5]
    
    # Get all routes for the sidebar
    routes = BusRoute.objects.all().order_by('bus_number')
    
    context = {
        'notifications': notifications,
        'routes': routes,
        'page_title': 'IUBAT Bus Tracker',
    }
    
    return render(request, 'user_panel/user_map.html', context)


def simulation_status(request):
    """
    Check if there are any real buses running or if we need simulation mode
    """
    recent_time = timezone.now() - timedelta(minutes=5)
    
    # Check for real (non-simulated) active locations
    real_buses = BusLocation.objects.filter(
        is_active=True,
        is_simulated=False,
        timestamp__gte=recent_time
    ).count()
    
    # Check for simulated locations
    simulated_buses = BusLocation.objects.filter(
        is_active=True,
        is_simulated=True,
        timestamp__gte=recent_time
    ).count()
    
    context = {
        'real_buses_count': real_buses,
        'simulated_buses_count': simulated_buses,
        'simulation_mode': real_buses == 0,
    }
    
    return render(request, 'user_panel/simulation_status.html', context)


def bus_schedule_list(request):
    """
    Display bus schedules for users
    """
    dhaka_tz = pytz.timezone('Asia/Dhaka')
    current_time_dhaka = timezone.now().astimezone(dhaka_tz)

    # Get the active schedule type from GlobalSettings
    global_settings, created = GlobalSettings.objects.get_or_create(pk=1)
    active_type_filter = global_settings.active_route_type

    # Fetch all bus routes with active schedules
    routes = BusRoute.objects.prefetch_related(
        Prefetch(
            'schedules',
            queryset=BusSchedule.objects.filter(
                route_type=active_type_filter,
                is_active=True
            ).order_by('departure_time')
        )
    ).all()

    context = {
        'routes': routes,
        'current_time': current_time_dhaka,
        'active_schedule_type_display': global_settings.get_active_route_type_display(),
        'active_schedule_type_raw': global_settings.active_route_type,
    }
    return render(request, 'user_panel/bus_schedule_list.html', context)


@login_required
def home_view(request):
    """
    Unified home page with navigation tabs for all users
    Content adapts based on user role
    """
    # Get statistics
    total_buses = BusRoute.objects.count()
    total_routes = BusRoute.objects.filter(is_shuttle=False).count()
    total_schedules = BusSchedule.objects.filter(is_active=True).count()
    
    # Get active buses (locations updated in last 10 minutes)
    recent_time = timezone.now() - timedelta(minutes=10)
    active_buses = BusLocation.objects.filter(
        timestamp__gte=recent_time,
        is_active=True
    ).values('bus').distinct().count()
    
    context = {
        'page_title': 'IUBAT Bus Management System',
        'total_buses': total_buses,
        'total_routes': total_routes,
        'total_schedules': total_schedules,
        'active_buses': active_buses,
    }
    
    return render(request, 'user_panel/home.html', context)
