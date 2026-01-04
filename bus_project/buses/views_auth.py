"""
Authentication Views - Unified Login System with Role-Based Redirect
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile


def unified_login(request):
    """
    Unified login view that redirects users based on their role
    - USER -> User Map
    - DRIVER -> Driver Dashboard
    - ADMIN/AUTHORITY -> Admin Dashboard
    """
    if request.user.is_authenticated:
        return redirect_based_on_role(request.user)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect_based_on_role(user)
        else:
            messages.error(request, "Invalid username or password.")

    return render(
        request, "buses/auth/login.html", {"page_title": "IUBAT Bus Management - Login"}
    )


def redirect_based_on_role(user):
    """Helper function to redirect users based on their role"""
    try:
        profile = user.profile
        if profile.role == "DRIVER":
            return redirect("buses:driver_dashboard")
        elif profile.role == "ADMIN" or user.is_staff:
            return redirect("buses:custom_admin_dashboard")
        else:
            # Regular USER or AUTHORITY
            return redirect("buses:home")
    except:
        # Fallback if profile doesn't exist
        return redirect("buses:home")


@login_required
def custom_logout(request):
    """Logout view that returns to login page"""
    username = request.user.username
    logout(request)
    messages.success(request, f"Goodbye, {username}! You have been logged out.")
    return redirect("buses:login")
