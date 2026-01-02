"""
User Map View - Main public-facing map interface for users to track buses
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import BusRoute, BusLocation, Notification
from django.utils import timezone
from datetime import timedelta


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
    
    return render(request, 'buses/user_map.html', context)


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
    
    return render(request, 'buses/simulation_status.html', context)
