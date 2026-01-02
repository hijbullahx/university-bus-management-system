"""
Admin and Authority Dashboard Views
For managing the system and viewing reports
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Q
from django.utils import timezone
from datetime import timedelta, datetime
from .models import (BusRoute, BusLocation, IssueReport, Notification, 
                     DriverRouteSession, UserProfile, BusSchedule)
import json


def require_admin_or_authority(view_func):
    """Decorator to ensure user is admin or authority"""
    @login_required
    def wrapper(request, *args, **kwargs):
        try:
            profile = request.user.profile
            if profile.role not in ['ADMIN', 'AUTHORITY']:
                messages.error(request, 'Access denied. Admins and Authority only.')
                return redirect('home')
        except UserProfile.DoesNotExist:
            messages.error(request, 'User profile not found.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@require_admin_or_authority
def admin_dashboard(request):
    """
    Main admin dashboard with overview statistics
    """
    # Get statistics
    total_buses = BusRoute.objects.count()
    total_routes = BusRoute.objects.filter(is_shuttle=False).count()
    total_shuttles = BusRoute.objects.filter(is_shuttle=True).count()
    
    # Active buses in last 5 minutes
    recent_time = timezone.now() - timedelta(minutes=5)
    active_buses = BusLocation.objects.filter(
        is_active=True,
        timestamp__gte=recent_time
    ).values('bus').distinct().count()
    
    # Pending issues
    pending_issues = IssueReport.objects.filter(status='PENDING').count()
    
    # Active route sessions
    active_sessions = DriverRouteSession.objects.filter(is_active=True).count()
    
    # Recent issues
    recent_issues = IssueReport.objects.select_related(
        'bus', 'driver'
    ).order_by('-timestamp')[:10]
    
    # Recent notifications
    recent_notifications = Notification.objects.order_by('-created_at')[:5]
    
    context = {
        'total_buses': total_buses,
        'total_routes': total_routes,
        'total_shuttles': total_shuttles,
        'active_buses': active_buses,
        'pending_issues': pending_issues,
        'active_sessions': active_sessions,
        'recent_issues': recent_issues,
        'recent_notifications': recent_notifications,
        'page_title': 'Admin Dashboard',
    }
    
    return render(request, 'buses/admin_dashboard_new.html', context)


@require_admin_or_authority
def admin_reports(request):
    """
    Reports page with Chart.js visualizations
    Shows dummy data for On-Time Performance and other metrics
    """
    # Get date range (last 7 days)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)
    
    # Issues by type
    issues_by_type = IssueReport.objects.filter(
        timestamp__gte=start_date
    ).values('issue_type').annotate(count=Count('id'))
    
    # Daily active buses for the last 7 days
    daily_active = []
    for i in range(7):
        day = start_date + timedelta(days=i)
        day_start = day.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        count = BusLocation.objects.filter(
            timestamp__gte=day_start,
            timestamp__lt=day_end,
            is_active=True
        ).values('bus').distinct().count()
        
        daily_active.append({
            'date': day.strftime('%Y-%m-%d'),
            'count': count
        })
    
    # Generate dummy on-time performance data (for demonstration)
    buses = BusRoute.objects.all()[:5]  # Top 5 buses
    on_time_data = []
    for bus in buses:
        # Random-ish but consistent data based on bus_id
        import random
        random.seed(bus.id)
        on_time_percentage = random.randint(75, 98)
        on_time_data.append({
            'bus_number': bus.bus_number,
            'route': bus.route,
            'on_time_percentage': on_time_percentage,
        })
    
    # Average session duration
    completed_sessions = DriverRouteSession.objects.filter(
        is_active=False,
        ended_at__isnull=False,
        started_at__gte=start_date
    )
    
    avg_duration_data = []
    for session in completed_sessions[:10]:
        duration = (session.ended_at - session.started_at).total_seconds() / 60  # minutes
        avg_duration_data.append({
            'bus': session.bus.bus_number,
            'driver': session.driver.username,
            'duration': round(duration, 2)
        })
    
    context = {
        'issues_by_type': list(issues_by_type),
        'daily_active': daily_active,
        'on_time_data': on_time_data,
        'avg_duration_data': avg_duration_data,
        'page_title': 'Reports & Analytics',
    }
    
    return render(request, 'buses/admin_reports.html', context)


@require_admin_or_authority
def admin_live_tracking(request):
    """
    Live tracking view for admins to see all buses on a map
    """
    buses = BusRoute.objects.all().order_by('bus_number')
    
    context = {
        'buses': buses,
        'page_title': 'Live Bus Tracking',
    }
    
    return render(request, 'buses/admin_live_tracking.html', context)


@require_admin_or_authority
def admin_manage_issues(request):
    """
    View all issues and manage them
    """
    status_filter = request.GET.get('status', 'all')
    
    issues = IssueReport.objects.select_related('bus', 'driver', 'resolved_by')
    
    if status_filter != 'all':
        issues = issues.filter(status=status_filter.upper())
    
    issues = issues.order_by('-timestamp')
    
    context = {
        'issues': issues,
        'status_filter': status_filter,
        'page_title': 'Manage Issues',
    }
    
    return render(request, 'buses/admin_manage_issues.html', context)


@require_admin_or_authority
def admin_manage_notifications(request):
    """
    Create and manage system notifications
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        notification_type = request.POST.get('notification_type')
        priority = request.POST.get('priority', 1)
        bus_id = request.POST.get('bus_id')
        
        notification = Notification.objects.create(
            title=title,
            message=message,
            notification_type=notification_type,
            priority=int(priority),
            bus_id=bus_id if bus_id else None,
            created_by=request.user
        )
        
        messages.success(request, 'Notification created successfully!')
        return redirect('admin_manage_notifications')
    
    notifications = Notification.objects.select_related('bus', 'created_by').order_by('-created_at')
    buses = BusRoute.objects.all().order_by('bus_number')
    
    context = {
        'notifications': notifications,
        'buses': buses,
        'page_title': 'Manage Notifications',
    }
    
    return render(request, 'buses/admin_manage_notifications.html', context)
