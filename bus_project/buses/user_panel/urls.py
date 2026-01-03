"""
User Panel URL Configuration
Public-facing routes for bus tracking and schedules
"""
from django.urls import path
from . import views

app_name = 'user_panel'

urlpatterns = [
    # Page Views
    path('', views.user_map_view, name='map'),
    path('map/', views.user_map_view, name='user_map'),
    path('schedules/', views.bus_schedule_list, name='schedules'),
    path('home/', views.home_view, name='home'),
    path('simulation-status/', views.simulation_status, name='simulation_status'),
    
    # API Endpoints (AJAX)
    path('api/map-data/', views.bus_map_data, name='api_map_data'),
    path('api/schedule-eta/', views.schedule_eta_api, name='api_schedule_eta'),
]

