from django.utils import timezone
import pytz # We'll need to install this package
from django.shortcuts import render
from .models import BusRoute, BusSchedule
from django.db.models import Prefetch

def bus_schedule_list(request):
    # Fetch all bus routes
    # Use Prefetch to efficiently get all schedules for each route in one query
    # We also order schedules by departure_time for consistent display
    routes = BusRoute.objects.prefetch_related(
        Prefetch(
            'schedules',
            queryset=BusSchedule.objects.order_by('departure_time', 'route_type')
        )
    ).all()

    context = {
        'routes': routes,
        'current_time': timezone.now().astimezone(pytz.timezone('Asia/Dhaka')), # Set current time to Dhaka timezone
    }
    return render(request, 'bus_schedule_list.html', context)