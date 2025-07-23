from django.urls import path
from . import views

app_name = 'buses' # Define the app namespace

urlpatterns = [
  path('', views.bus_schedule_list, name = 'bus_schedule_list'), # Route for bus schedule list
]