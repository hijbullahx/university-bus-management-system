from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from ..models import BusRoute, BusSchedule, UserProfile, IssueReport, Notification, BusLocation
from django.utils import timezone
from datetime import timedelta

def authority_required(view_func):
    """Decorator to check if user has AUTHORITY role"""
    return user_passes_test(lambda u: hasattr(u, 'profile') and u.profile.role == 'AUTHORITY')(view_func)

@login_required
@authority_required
def authority_dashboard(request):
    """Authority dashboard with system overview"""
    # System statistics
    total_routes = BusRoute.objects.count()
    total_schedules = BusSchedule.objects.count()
    total_users = UserProfile.objects.count()
    active_issues = IssueReport.objects.filter(status='OPEN').count()
    total_notifications = Notification.objects.count()

    # Role distribution
    role_counts = {
        'USER': UserProfile.objects.filter(role='USER').count(),
        'DRIVER': UserProfile.objects.filter(role='DRIVER').count(),
        'ADMIN': UserProfile.objects.filter(role='ADMIN').count(),
        'AUTHORITY': UserProfile.objects.filter(role='AUTHORITY').count(),
    }

    # Live bus locations (active in last 10 minutes)
    recent_time = timezone.now() - timedelta(minutes=10)
    active_locations = BusLocation.objects.filter(
        timestamp__gte=recent_time,
        is_active=True
    ).select_related('bus').order_by('-timestamp')

    context = {
        'total_routes': total_routes,
        'total_schedules': total_schedules,
        'total_users': total_users,
        'active_issues': active_issues,
        'total_notifications': total_notifications,
        'role_counts': role_counts,
        'active_locations': active_locations,
    }
    return render(request, 'buses/authority/dashboard.html', context)