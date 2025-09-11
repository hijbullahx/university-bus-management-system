from rest_framework import routers
from .api_views import BusRouteViewSet, BusScheduleViewSet, GlobalSettingsViewSet

router = routers.DefaultRouter()
router.register(r'routes', BusRouteViewSet)
router.register(r'schedules', BusScheduleViewSet)
router.register(r'global-settings', GlobalSettingsViewSet)

urlpatterns = router.urls
