from rest_framework import serializers
from .models import BusRoute, BusSchedule, GlobalSettings

class BusRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusRoute
        fields = '__all__'

class BusScheduleSerializer(serializers.ModelSerializer):
    route = BusRouteSerializer(read_only=True)
    route_id = serializers.PrimaryKeyRelatedField(queryset=BusRoute.objects.all(), source='route', write_only=True)

    class Meta:
        model = BusSchedule
        fields = ['id', 'route', 'route_id', 'departure_time', 'arrival_time', 'is_active', 'route_type', 'notes']

class GlobalSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalSettings
        fields = '__all__'
