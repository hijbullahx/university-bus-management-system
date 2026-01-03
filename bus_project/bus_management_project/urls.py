
from django.contrib import admin
from buses.admin import custom_admin_site
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_home(request):
    """Redirect root URL to unified home page"""
    if request.user.is_authenticated:
        return redirect('buses:home')
    return redirect('buses:login')


def redirect_logout(request):
    """Redirect legacy /logout/ to buses logout view"""
    return redirect('buses:logout')

urlpatterns = [
    path("admin/", custom_admin_site.urls),  # Django admin panel
    path("", redirect_to_home),  # Root redirects to home or login
    path("logout/", redirect_logout),  # Legacy logout path -> app logout
    path("buses/", include("buses.urls")),  # Main buses app URLs
    path("api/", include("buses.api_urls")),  # API endpoints for REST framework
]
