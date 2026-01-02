"""
Home View - Unified interface with role-based navigation
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import BusRoute, BusSchedule, BusLocation


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
    
    return render(request, 'buses/home.html', context)
