"""
User Panel URL Configuration
Public-facing routes for bus tracking and schedules
"""
from django.urls import path
from . import views

app_name = 'user_panel'

urlpatterns = [
    # Main user map view
    path('', views.user_map_view, name='map'),
    path('map/', views.user_map_view, name='user_map'),
    
    # Bus schedules
    path('schedules/', views.bus_schedule_list, name='schedules'),
    
    # Home view (for logged-in users)
    path('home/', views.home_view, name='home'),
    
    # Simulation status
    path('simulation-status/', views.simulation_status, name='simulation_status'),
]
