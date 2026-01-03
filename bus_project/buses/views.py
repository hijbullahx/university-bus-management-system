from django.shortcuts import render
from .models import BusRoute, BusSchedule
from django.db.models import Prefetch
from django.utils import timezone
import pytz

def bus_schedule_list(request):
    dhaka_tz = pytz.timezone('Asia/Dhaka')
    current_time_dhaka = timezone.now().astimezone(dhaka_tz)

    # Default to showing REGULAR schedules (GlobalSettings removed)
    active_type_filter = 'REGULAR'

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
        'active_schedule_type_display': 'Regular Schedule',
        'active_schedule_type_raw': active_type_filter,
    }
    return render(request, 'bus_schedule_list.html', context) # Assumes template is in project-level templates