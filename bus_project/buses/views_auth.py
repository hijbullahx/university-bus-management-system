"""
Authentication Views - Unified Login System with Role-Based Redirect
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.models import User


def unified_login(request):
    """
    Unified login view that redirects users based on their role
    - USER -> User Map
    - DRIVER -> Driver Dashboard
    - ADMIN/AUTHORITY -> Admin Dashboard
    """
    if request.user.is_authenticated:
        return redirect_based_on_role(request.user)
    
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # Allow users to login with either username or email
        username = username_or_email
        if username_or_email and '@' in username_or_email:
            try:
                user_obj = User.objects.get(email__iexact=username_or_email)
                username = user_obj.username
            except User.DoesNotExist:
                # fall back to using the provided value as username
                username = username_or_email

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect_based_on_role(user)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'buses/auth/login.html', {
        'page_title': 'IUBAT Bus Management - Login'
    })


def redirect_based_on_role(user):
    """Helper function to redirect users to unified home page"""
    if hasattr(user, 'profile'):
        if user.profile.role == 'AUTHORITY':
            return redirect('buses:authority_dashboard')
    # Everyone else goes to the unified home page
    # Navigation tabs will adapt based on their role
    return redirect('buses:home')


@login_required
def custom_logout(request):
    """Logout view that returns to the unified home page"""
    username = request.user.username
    # Log out user and ensure session data is removed
    logout(request)
    try:
        request.session.flush()
    except Exception:
        pass

    messages.success(request, f'Goodbye, {username}! You have been logged out.')
    response = redirect('buses:login')

    # Remove session and CSRF cookies from client
    session_cookie = getattr(settings, 'SESSION_COOKIE_NAME', 'sessionid')
    csrf_cookie = getattr(settings, 'CSRF_COOKIE_NAME', 'csrftoken')
    response.delete_cookie(session_cookie)
    response.delete_cookie(csrf_cookie)
    return response
