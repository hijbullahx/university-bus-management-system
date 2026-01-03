from django.urls import path
from rest_framework import routers
from .api_views import (BusRouteViewSet, BusScheduleViewSet,
                        BusLocationViewSet, IssueReportViewSet, NotificationViewSet,
                        DriverRouteSessionViewSet, bus_map_data)

router = routers.DefaultRouter()
router.register(r'routes', BusRouteViewSet)
router.register(r'schedules', BusScheduleViewSet)
router.register(r'bus-locations', BusLocationViewSet)
router.register(r'issues', IssueReportViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'driver-sessions', DriverRouteSessionViewSet)

urlpatterns = [
    path('map-data/', bus_map_data, name='bus-map-data'),
] + router.urls

