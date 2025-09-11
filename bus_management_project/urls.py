
from django.contrib import admin
from buses.admin import custom_admin_site
from django.urls import path, include

urlpatterns = [
    path("admin/", custom_admin_site.urls),
    path("", include("buses.urls")), # Include the buses app URLs
    path("api/", include("buses.api_urls")), # API endpoints for REST framework
]
