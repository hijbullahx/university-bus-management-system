from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import (BusRoute, BusSchedule, GlobalSettings, BusLocation, 
                     IssueReport, Notification, UserProfile, DriverRouteSession)
from .serializers import (BusRouteSerializer, BusScheduleSerializer, GlobalSettingsSerializer,
                          BusLocationSerializer, BusLocationCreateSerializer, IssueReportSerializer,
                          NotificationSerializer, UserProfileSerializer, DriverRouteSessionSerializer,
                          BusRouteDetailSerializer)


class BusRouteViewSet(viewsets.ModelViewSet):
    queryset = BusRoute.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BusRouteDetailSerializer
        return BusRouteSerializer
    
    @action(detail=True, methods=['get'])
    def current_location(self, request, pk=None):
        """Get the most recent location for this bus"""
        bus = self.get_object()
        location = BusLocation.objects.filter(
            bus=bus, 
            is_active=True,
            timestamp__gte=timezone.now() - timedelta(minutes=5)
        ).first()
        
        if location:
            serializer = BusLocationSerializer(location)
            return Response(serializer.data)
        return Response({'message': 'No recent location data'}, status=status.HTTP_404_NOT_FOUND)


class BusScheduleViewSet(viewsets.ModelViewSet):
    queryset = BusSchedule.objects.select_related('route').all()
    serializer_class = BusScheduleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class GlobalSettingsViewSet(viewsets.ModelViewSet):
    queryset = GlobalSettings.objects.all()
    serializer_class = GlobalSettingsSerializer
    permission_classes = [permissions.IsAdminUser]


class BusLocationViewSet(viewsets.ModelViewSet):
    queryset = BusLocation.objects.select_related('bus', 'driver').all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BusLocationCreateSerializer
        return BusLocationSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter active buses (locations within last 5 minutes)
        active_only = self.request.query_params.get('active', None)
        if active_only:
            queryset = queryset.filter(
                is_active=True,
                timestamp__gte=timezone.now() - timedelta(minutes=5)
            )
        
        # Filter by bus
        bus_id = self.request.query_params.get('bus', None)
        if bus_id:
            queryset = queryset.filter(bus_id=bus_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def active_buses(self, request):
        """Get the latest location for all active buses"""
        # Get the most recent location for each bus within the last 5 minutes
        recent_time = timezone.now() - timedelta(minutes=5)
        buses = BusRoute.objects.all()
        active_locations = []
        
        for bus in buses:
            location = BusLocation.objects.filter(
                bus=bus,
                is_active=True,
                timestamp__gte=recent_time
            ).first()
            
            if location:
                active_locations.append(location)
        
        serializer = BusLocationSerializer(active_locations, many=True)
        return Response(serializer.data)


class IssueReportViewSet(viewsets.ModelViewSet):
    queryset = IssueReport.objects.select_related('bus', 'driver', 'resolved_by').all()
    serializer_class = IssueReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(driver=self.request.user)
    
    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        """Mark an issue as resolved"""
        issue = self.get_object()
        issue.status = 'RESOLVED'
        issue.resolved_at = timezone.now()
        issue.resolved_by = request.user
        issue.save()
        
        serializer = self.get_serializer(issue)
        return Response(serializer.data)


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.select_related('bus', 'created_by').all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter active notifications
        active_only = self.request.query_params.get('active', 'true')
        if active_only.lower() == 'true':
            queryset = queryset.filter(is_active=True)
        
        return queryset


class DriverRouteSessionViewSet(viewsets.ModelViewSet):
    queryset = DriverRouteSession.objects.select_related('driver', 'bus').all()
    serializer_class = DriverRouteSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Drivers can only see their own sessions
        if hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'DRIVER':
            queryset = queryset.filter(driver=self.request.user)
        
        return queryset
    
    @action(detail=False, methods=['post'])
    def start_route(self, request):
        """Start a new route session for the driver"""
        bus_id = request.data.get('bus_id')
        
        if not bus_id:
            return Response({'error': 'bus_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if driver already has an active session
        active_session = DriverRouteSession.objects.filter(
            driver=request.user,
            is_active=True
        ).first()
        
        if active_session:
            return Response({
                'error': 'You already have an active route session',
                'session_id': active_session.id
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            bus = BusRoute.objects.get(id=bus_id)
        except BusRoute.DoesNotExist:
            return Response({'error': 'Bus not found'}, status=status.HTTP_404_NOT_FOUND)
        
        session = DriverRouteSession.objects.create(
            driver=request.user,
            bus=bus
        )
        
        serializer = self.get_serializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def end_route(self, request, pk=None):
        """End an active route session"""
        session = self.get_object()
        
        if not session.is_active:
            return Response({'error': 'Session is already ended'}, status=status.HTTP_400_BAD_REQUEST)
        
        session.ended_at = timezone.now()
        session.is_active = False
        session.save()
        
        serializer = self.get_serializer(session)
        return Response(serializer.data)


# NOTE: bus_map_data() has been moved to buses.user_panel.api_views
# This keeps user-centric code organized within the user_panel module
# Legacy compatibility is maintained in api_urls.py

