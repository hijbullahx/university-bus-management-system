"""
User Panel Views - Public-facing map interface for users to track buses
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from buses.models import BusRoute, BusLocation, Notification, BusSchedule, GlobalSettings
from django.utils import timezone
from datetime import timedelta
from django.db.models import Prefetch
from math import radians, cos, sin, sqrt, atan2
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
    Display bus schedules for users with stops and live ETA
    """
    dhaka_tz = pytz.timezone('Asia/Dhaka')
    current_time_dhaka = timezone.now().astimezone(dhaka_tz)

    # Get the active schedule type from GlobalSettings
    global_settings, created = GlobalSettings.objects.get_or_create(pk=1)
    active_type_filter = global_settings.active_route_type

    # Fetch all bus routes with active schedules and stopages
    routes = BusRoute.objects.prefetch_related(
        Prefetch(
            'schedules',
            queryset=BusSchedule.objects.filter(
                route_type=active_type_filter,
                is_active=True
            ).order_by('departure_time')
        ),
        'stopages'  # Also fetch stopages for each route
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


# ============================================================================
# API Views for User Panel (AJAX endpoints)
# ============================================================================

def bus_map_data(request):
    """
    API endpoint returning active bus locations with ETA and next stop info
    Used by the live map interface
    """
    def calculate_distance(lat1, lon1, lat2, lon2):
        """Haversine formula for distance calculation"""
        R = 6371
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        return R * 2 * atan2(sqrt(a), sqrt(1-a))
    
    def find_next_stop(bus, current_lat, current_lon):
        """Find next stop based on time"""
        stopages = bus.stopages.all().order_by('pickup_time')
        if not stopages:
            return None, None
        
        current_time = timezone.now().time()
        for stop in stopages:
            if stop.pickup_time > current_time:
                return stop, 2.0  # Default 2km distance
        
        return stopages.first(), 3.0  # Loop back to first
    
    def calculate_eta(distance, speed):
        """Calculate ETA in minutes"""
        speed = speed if speed > 0 else 30
        return int((distance / speed) * 60)
    
    # Query parameters
    recent_time = timezone.now() - timedelta(minutes=5)
    route_filter = request.GET.get('route')
    
    buses = BusRoute.objects.filter(id=route_filter) if route_filter else BusRoute.objects.all()
    
    map_data = []
    for bus in buses:
        location = BusLocation.objects.filter(
            bus=bus, is_active=True, timestamp__gte=recent_time
        ).order_by('-timestamp').first()
        
        if location:
            next_stop, distance = find_next_stop(bus, location.latitude, location.longitude)
            eta_minutes = calculate_eta(distance, location.speed) if next_stop else None
            
            map_data.append({
                'bus_id': bus.id,
                'bus_number': bus.bus_number,
                'route': bus.route,
                'latitude': float(location.latitude),
                'longitude': float(location.longitude),
                'speed': float(location.speed),
                'timestamp': location.timestamp.isoformat(),
                'is_simulated': location.is_simulated,
                'next_stop': next_stop.name if next_stop else 'No upcoming stops',
                'eta_minutes': eta_minutes,
                'distance_to_next_stop': round(distance, 2) if distance else None,
            })
    
    return JsonResponse({
        'buses': map_data,
        'total_active': len(map_data),
        'routes': list(BusRoute.objects.values('id', 'bus_number', 'route')),
        'timestamp': timezone.now().isoformat(),
    })


def schedule_eta_api(request):
    """
    API endpoint to provide live ETA for each stop on each route
    Returns schedule data with real-time ETA calculations
    """
    from buses.models import Stopage
    
    route_id = request.GET.get('route_id')
    recent_time = timezone.now() - timedelta(minutes=10)
    
    # Get active routes or specific route
    if route_id:
        routes = BusRoute.objects.filter(id=route_id)
    else:
        routes = BusRoute.objects.all()
    
    routes_data = []
    
    for route in routes:
        # Get latest bus location for this route
        latest_location = BusLocation.objects.filter(
            bus=route,
            is_active=True,
            timestamp__gte=recent_time
        ).order_by('-timestamp').first()
        
        # Get all stopages for this route
        stopages = route.stopages.all().order_by('pickup_time')
        stops_data = []
        
        for stop in stopages:
            stop_data = {
                'name': stop.name,
                'scheduled_time': stop.pickup_time.strftime('%I:%M %p'),
                'scheduled_time_raw': stop.pickup_time.strftime('%H:%M'),
            }
            
            # Calculate live ETA if bus is active
            if latest_location:
                # Find bus's current position and calculate ETA
                current_time = timezone.now()
                scheduled_dt = timezone.make_aware(
                    timezone.datetime.combine(current_time.date(), stop.pickup_time)
                )
                
                # Simple ETA estimation (in production, use actual GPS coordinates)
                time_diff = (scheduled_dt - current_time).total_seconds() / 60  # minutes
                
                if time_diff < -5:  # Stop already passed
                    stop_data['eta'] = 'Passed'
                    stop_data['eta_status'] = 'passed'
                elif time_diff < 0:  # At stop or just passed
                    stop_data['eta'] = 'Now'
                    stop_data['eta_status'] = 'now'
                else:
                    eta_minutes = int(time_diff)
                    stop_data['eta'] = f"{eta_minutes} min"
                    # Determine if on-time (green) or delayed (red)
                    if eta_minutes <= int(time_diff) + 3:
                        stop_data['eta_status'] = 'on-time'
                    else:
                        stop_data['eta_status'] = 'delayed'
            else:
                stop_data['eta'] = 'No bus active'
                stop_data['eta_status'] = 'inactive'
            
            stops_data.append(stop_data)
        
        routes_data.append({
            'id': route.id,
            'bus_number': route.bus_number,
            'route': route.route,
            'is_active': latest_location is not None,
            'stops': stops_data,
        })
    
    return JsonResponse({
        'routes': routes_data,
        'timestamp': timezone.now().isoformat(),
    })


def schedule_eta_api(request):
    """
    API endpoint to provide live ETA for each stop on each route
    Returns schedule data with real-time ETA calculations
    """
    route_id = request.GET.get('route_id')
    recent_time = timezone.now() - timedelta(minutes=10)
    
    # Get active routes or specific route
    if route_id:
        routes = BusRoute.objects.filter(id=route_id)
    else:
        routes = BusRoute.objects.all()
    
    routes_data = []
    
    for route in routes:
        # Get latest bus location for this route
        latest_location = BusLocation.objects.filter(
            bus=route,
            is_active=True,
            timestamp__gte=recent_time
        ).order_by('-timestamp').first()
        
        # Get all stopages for this route
        stopages = route.stopages.all().order_by('pickup_time')
        stops_data = []
        
        for stop in stopages:
            stop_data = {
                'name': stop.name,
                'scheduled_time': stop.pickup_time.strftime('%I:%M %p'),
                'scheduled_time_raw': stop.pickup_time.strftime('%H:%M'),
            }
            
            # Calculate live ETA if bus is active
            if latest_location:
                # Find bus's current position and calculate ETA
                current_time = timezone.now()
                scheduled_dt = timezone.make_aware(
                    timezone.datetime.combine(current_time.date(), stop.pickup_time)
                )
                
                # Simple ETA estimation (in production, use actual GPS coordinates)
                time_diff = (scheduled_dt - current_time).total_seconds() / 60  # minutes
                
                if time_diff < -5:  # Stop already passed
                    stop_data['eta'] = 'Passed'
                    stop_data['eta_status'] = 'passed'
                elif time_diff < 0:  # At stop or just passed
                    stop_data['eta'] = 'Now'
                    stop_data['eta_status'] = 'now'
                else:
                    eta_minutes = int(time_diff)
                    stop_data['eta'] = f"{eta_minutes} min"
                    # Determine if on-time (green) or delayed (red)
                    if eta_minutes <= int(time_diff) + 3:
                        stop_data['eta_status'] = 'on-time'
                    else:
                        stop_data['eta_status'] = 'delayed'
            else:
                stop_data['eta'] = 'No bus active'
                stop_data['eta_status'] = 'inactive'
            
            stops_data.append(stop_data)
        
        routes_data.append({
            'id': route.id,
            'bus_number': route.bus_number,
            'route': route.route,
            'is_active': latest_location is not None,
            'stops': stops_data,
        })
    
    return JsonResponse({
        'routes': routes_data,
        'timestamp': timezone.now().isoformat(),
    })

