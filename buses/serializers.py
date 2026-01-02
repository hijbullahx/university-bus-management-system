from rest_framework import serializers
from .models import (BusRoute, BusSchedule, GlobalSettings, BusLocation, 
                     IssueReport, Notification, UserProfile, DriverRouteSession, Stopage)

class BusRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusRoute
        fields = '__all__'


class StopageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stopage
        fields = ['id', 'name', 'pickup_time']


class BusRouteDetailSerializer(serializers.ModelSerializer):
    stopages = StopageSerializer(many=True, read_only=True)
    
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


class BusLocationSerializer(serializers.ModelSerializer):
    bus_number = serializers.CharField(source='bus.bus_number', read_only=True)
    bus_route = serializers.CharField(source='bus.route', read_only=True)
    driver_name = serializers.CharField(source='driver.username', read_only=True)
    
    class Meta:
        model = BusLocation
        fields = ['id', 'bus', 'bus_number', 'bus_route', 'driver', 'driver_name', 
                  'latitude', 'longitude', 'timestamp', 'speed', 'is_active', 'is_simulated']
        read_only_fields = ['timestamp']


class BusLocationCreateSerializer(serializers.ModelSerializer):
    """Serializer for drivers to create location updates"""
    class Meta:
        model = BusLocation
        fields = ['bus', 'latitude', 'longitude', 'speed', 'is_active']
    
    def create(self, validated_data):
        # Automatically add the driver from request.user
        validated_data['driver'] = self.context['request'].user
        return super().create(validated_data)


class IssueReportSerializer(serializers.ModelSerializer):
    driver_name = serializers.CharField(source='driver.username', read_only=True)
    bus_number = serializers.CharField(source='bus.bus_number', read_only=True)
    resolved_by_name = serializers.CharField(source='resolved_by.username', read_only=True)
    
    class Meta:
        model = IssueReport
        fields = ['id', 'bus', 'bus_number', 'driver', 'driver_name', 'issue_type', 
                  'description', 'location_lat', 'location_lng', 'timestamp', 'status', 
                  'resolved_at', 'resolved_by', 'resolved_by_name']
        read_only_fields = ['timestamp', 'driver']


class NotificationSerializer(serializers.ModelSerializer):
    bus_number = serializers.CharField(source='bus.bus_number', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'notification_type', 'bus', 'bus_number', 
                  'created_by', 'created_by_name', 'created_at', 'is_active', 'priority']
        read_only_fields = ['created_at', 'created_by']


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    assigned_bus_number = serializers.CharField(source='assigned_bus.bus_number', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'username', 'email', 'role', 'phone_number', 
                  'assigned_bus', 'assigned_bus_number']


class DriverRouteSessionSerializer(serializers.ModelSerializer):
    driver_name = serializers.CharField(source='driver.username', read_only=True)
    bus_number = serializers.CharField(source='bus.bus_number', read_only=True)
    duration = serializers.SerializerMethodField()
    
    class Meta:
        model = DriverRouteSession
        fields = ['id', 'driver', 'driver_name', 'bus', 'bus_number', 'started_at', 
                  'ended_at', 'is_active', 'total_distance', 'duration']
        read_only_fields = ['started_at']
    
    def get_duration(self, obj):
        if obj.ended_at:
            duration = obj.ended_at - obj.started_at
            return str(duration)
        return "Ongoing"

