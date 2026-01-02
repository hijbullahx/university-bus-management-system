
from django.contrib import admin
from buses.admin import custom_admin_site
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_map(request):
    """Redirect root URL to user map"""
    return redirect('buses:user_map')

urlpatterns = [
    path("admin/", custom_admin_site.urls),  # Django admin panel
    path("", redirect_to_map),  # Root redirects to map
    path("buses/", include("buses.urls")),  # Main buses app URLs
    path("api/", include("buses.api_urls")),  # API endpoints for REST framework
]
