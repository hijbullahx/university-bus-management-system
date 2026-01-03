from django.urls import path, include
from rest_framework import routers
from .api_views import (BusRouteViewSet, BusScheduleViewSet, GlobalSettingsViewSet,
                        BusLocationViewSet, IssueReportViewSet, NotificationViewSet,
                        DriverRouteSessionViewSet)

# Common API viewsets (admin, driver, shared endpoints)
router = routers.DefaultRouter()
router.register(r'routes', BusRouteViewSet)
router.register(r'schedules', BusScheduleViewSet)
router.register(r'global-settings', GlobalSettingsViewSet)
router.register(r'bus-locations', BusLocationViewSet)
router.register(r'issues', IssueReportViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'driver-sessions', DriverRouteSessionViewSet)

urlpatterns = [
    # User Panel API (map data, etc.) - legacy compatibility
    path('user/map-data/', lambda r: __import__('buses.user_panel.views', fromlist=['bus_map_data']).bus_map_data(r), name='user-map-data'),
    path('map-data/', lambda r: __import__('buses.user_panel.views', fromlist=['bus_map_data']).bus_map_data(r), name='map-data-legacy'),
] + router.urls


