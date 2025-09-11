from rest_framework import viewsets, permissions
from .models import BusRoute, BusSchedule, GlobalSettings
from .serializers import BusRouteSerializer, BusScheduleSerializer, GlobalSettingsSerializer

class BusRouteViewSet(viewsets.ModelViewSet):
    queryset = BusRoute.objects.all()
    serializer_class = BusRouteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BusScheduleViewSet(viewsets.ModelViewSet):
    queryset = BusSchedule.objects.select_related('route').all()
    serializer_class = BusScheduleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class GlobalSettingsViewSet(viewsets.ModelViewSet):
    queryset = GlobalSettings.objects.all()
    serializer_class = GlobalSettingsSerializer
    permission_classes = [permissions.IsAdminUser]
