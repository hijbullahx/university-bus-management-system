"""
Driver Dashboard Views
Mobile-responsive interface for drivers to start routes and update GPS location
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from .models import (
    BusRoute,
    DriverRouteSession,
    BusLocation,
    IssueReport,
    UserProfile,
    BusSchedule,
    GlobalSettings,
)
from django.db.models import Prefetch
import json
import pytz


@login_required
def driver_dashboard(request):
    """
    Main dashboard for drivers
    Shows assigned bus, active route session, and quick actions
    """
    try:
        profile = request.user.profile
        if profile.role != "DRIVER":
            messages.error(request, "Access denied. Drivers only.")
            return redirect("buses:home")
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect("buses:home")

    # Get active session
    active_session = (
        DriverRouteSession.objects.filter(driver=request.user, is_active=True)
        .select_related("bus")
        .first()
    )

    # Get assigned bus
    assigned_bus = profile.assigned_bus

    # Get recent issues reported by this driver
    recent_issues = (
        IssueReport.objects.filter(driver=request.user)
        .select_related("bus")
        .order_by("-timestamp")[:5]
    )

    context = {
        "active_session": active_session,
        "assigned_bus": assigned_bus,
        "recent_issues": recent_issues,
        "page_title": "Driver Dashboard",
    }

    return render(request, "buses/driver_dashboard.html", context)


@login_required
def driver_start_route(request):
    """
    View to start a new route session
    """
    if request.method == "POST":
        bus_id = request.POST.get("bus_id")

        # Check if already has active session
        active_session = DriverRouteSession.objects.filter(
            driver=request.user, is_active=True
        ).first()

        if active_session:
            messages.warning(
                request, "You already have an active route. Please end it first."
            )
            return redirect("buses:driver_dashboard")

        try:
            bus = BusRoute.objects.get(id=bus_id)
            session = DriverRouteSession.objects.create(driver=request.user, bus=bus)
            messages.success(request, f"Route started for {bus.bus_number}!")
            return redirect("buses:driver_tracking")
        except BusRoute.DoesNotExist:
            messages.error(request, "Bus not found.")
            return redirect("buses:driver_dashboard")

    # GET request - show available buses
    buses = BusRoute.objects.all().order_by("bus_number")

    context = {
        "buses": buses,
        "page_title": "Start Route",
    }

    return render(request, "buses/driver_start_route.html", context)


@login_required
def driver_tracking(request):
    """
    Active tracking view - GPS tracking interface
    Uses JavaScript Geolocation API to POST location every 10 seconds
    """
    active_session = (
        DriverRouteSession.objects.filter(driver=request.user, is_active=True)
        .select_related("bus")
        .first()
    )

    if not active_session:
        messages.warning(
            request, "No active route session. Please start a route first."
        )
        return redirect("buses:driver_start_route")

    context = {
        "active_session": active_session,
        "page_title": "Active Tracking",
    }

    return render(request, "buses/driver_tracking.html", context)


@login_required
@require_http_methods(["POST"])
def driver_end_route(request):
    """
    End the current active route session
    """
    active_session = DriverRouteSession.objects.filter(
        driver=request.user, is_active=True
    ).first()

    if not active_session:
        messages.warning(request, "No active route session found.")
        return redirect("buses:driver_dashboard")

    # End the session
    active_session.ended_at = timezone.now()
    active_session.is_active = False
    active_session.save()

    # Mark last location as inactive
    BusLocation.objects.filter(
        bus=active_session.bus, driver=request.user, is_active=True
    ).update(is_active=False)

    messages.success(request, "Route ended successfully!")
    return redirect("buses:driver_dashboard")


@login_required
def driver_report_issue(request):
    """
    View for drivers to report issues
    """
    if request.method == "POST":
        issue_type = request.POST.get("issue_type")
        description = request.POST.get("description")
        location_lat = request.POST.get("latitude")
        location_lng = request.POST.get("longitude")

        # Get active session to determine the bus
        active_session = DriverRouteSession.objects.filter(
            driver=request.user, is_active=True
        ).first()

        if not active_session:
            messages.error(request, "No active route session. Cannot report issue.")
            return redirect("buses:driver_dashboard")

        issue = IssueReport.objects.create(
            bus=active_session.bus,
            driver=request.user,
            issue_type=issue_type,
            description=description,
            location_lat=float(location_lat) if location_lat else None,
            location_lng=float(location_lng) if location_lng else None,
        )

        messages.success(request, "Issue reported successfully!")

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"success": True, "issue_id": issue.id})

        return redirect("buses:driver_dashboard")

    context = {
        "page_title": "Report Issue",
    }

    return render(request, "buses/driver_report_issue.html", context)


@login_required
def driver_schedules(request):
    """
    View schedules for the driver's assigned bus routes
    Shows departure times and stops
    """
    try:
        profile = request.user.profile
        if profile.role != "DRIVER":
            messages.error(request, "Access denied. Drivers only.")
            return redirect("buses:home")
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect("buses:home")

    dhaka_tz = pytz.timezone("Asia/Dhaka")
    current_time_dhaka = timezone.now().astimezone(dhaka_tz)

    # Get the active schedule type from GlobalSettings
    global_settings, created = GlobalSettings.objects.get_or_create(pk=1)
    active_type_filter = global_settings.active_route_type

    # If driver has assigned bus, show that bus's schedules first
    assigned_bus = profile.assigned_bus

    # Fetch all bus routes with active schedules
    routes = BusRoute.objects.prefetch_related(
        Prefetch(
            "schedules",
            queryset=BusSchedule.objects.filter(
                route_type=active_type_filter, is_active=True
            ).order_by("departure_time"),
        ),
        "stopages",
    ).all()

    context = {
        "routes": routes,
        "assigned_bus": assigned_bus,
        "current_time": current_time_dhaka,
        "active_schedule_type_display": global_settings.get_active_route_type_display(),
        "active_schedule_type_raw": global_settings.active_route_type,
        "page_title": "Driver Schedules",
    }

    return render(request, "buses/driver_schedules.html", context)
