from django.shortcuts import render
from .models import BusRoute, BusSchedule, GlobalSettings # Import GlobalSettings
from django.db.models import Prefetch
from django.utils import timezone
import pytz

def bus_schedule_list(request):
    dhaka_tz = pytz.timezone('Asia/Dhaka')
    current_time_dhaka = timezone.now().astimezone(dhaka_tz)

    # Get the active schedule type from GlobalSettings
    # Create one if it doesn't exist (e.g., on first run)
    global_settings, created = GlobalSettings.objects.get_or_create(pk=1) # Using pk=1 to ensure singleton
    active_type_filter = global_settings.active_route_type

    # Fetch all bus routes
    # Use Prefetch to efficiently get only active schedules for each route
    routes = BusRoute.objects.prefetch_related(
        Prefetch(
            'schedules',
            queryset=BusSchedule.objects.filter(
                route_type=active_type_filter, # Filter by active type
                is_active=True # Keep this filter for individual schedule activation
            ).order_by('departure_time')
        )
    ).all()

    context = {
        'routes': routes,
        'current_time': current_time_dhaka,
        'active_schedule_type_display': global_settings.get_active_route_type_display(), # Pass for display
        'active_schedule_type_raw': global_settings.active_route_type, # Pass for potential future filtering UI
    }
    return render(request, 'bus_schedule_list.html', context) # Assumes template is in project-level templates