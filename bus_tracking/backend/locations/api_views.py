from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from .models import DriverLocation, LocationHistory
from .serializers import DriverLocationSerializer, LocationUpdateSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_location(request):
    """Update driver's live location."""
    if request.user.role != 'driver':
        return Response(
            {'error': 'Only drivers can share location'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = LocationUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    data = serializer.validated_data
    
    # Update or create driver location
    location, created = DriverLocation.objects.update_or_create(
        driver=request.user,
        defaults={
            'latitude': data['latitude'],
            'longitude': data['longitude'],
            'accuracy': data.get('accuracy'),
            'heading': data.get('heading'),
            'speed': data.get('speed'),
            'is_sharing': True,
            'session_started': timezone.now() if created else None
        }
    )
    
    # Set session start time if just started sharing
    if created or not location.session_started:
        location.session_started = timezone.now()
        location.save(update_fields=['session_started'])
    
    return Response({
        'status': 'success',
        'message': 'Location updated',
        'timestamp': location.last_updated.isoformat()
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_sharing(request):
    """Start location sharing session."""
    if request.user.role != 'driver':
        return Response(
            {'error': 'Only drivers can share location'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    location, created = DriverLocation.objects.get_or_create(
        driver=request.user,
        defaults={'latitude': 0, 'longitude': 0}
    )
    location.is_sharing = True
    location.session_started = timezone.now()
    location.save()
    
    return Response({
        'status': 'success',
        'message': 'Location sharing started'
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def stop_sharing(request):
    """Stop location sharing session."""
    if request.user.role != 'driver':
        return Response(
            {'error': 'Only drivers can share location'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        location = DriverLocation.objects.get(driver=request.user)
        location.is_sharing = False
        location.save(update_fields=['is_sharing'])
        
        return Response({
            'status': 'success',
            'message': 'Location sharing stopped'
        })
    except DriverLocation.DoesNotExist:
        return Response({
            'status': 'success',
            'message': 'No active sharing session'
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_active_locations(request):
    """Get all active driver locations based on user role."""
    # Expire stale locations first
    DriverLocation.expire_inactive()
    
    active_locations = DriverLocation.get_active_drivers()
    
    # Role-based filtering
    if request.user.role in ['admin', 'authority']:
        # Admin/Authority see all active drivers
        pass
    elif request.user.role == 'driver':
        # Drivers see all active drivers
        pass
    else:
        # Regular users see only drivers on active routes
        # For now, show all active - can be restricted later
        pass
    
    serializer = DriverLocationSerializer(active_locations, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_location_status(request):
    """Get current user's location sharing status."""
    if request.user.role != 'driver':
        return Response(
            {'error': 'Only drivers have location status'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        location = DriverLocation.objects.get(driver=request.user)
        return Response({
            'is_sharing': location.is_sharing,
            'is_active': location.is_active,
            'last_updated': location.last_updated.isoformat() if location.last_updated else None,
            'session_started': location.session_started.isoformat() if location.session_started else None
        })
    except DriverLocation.DoesNotExist:
        return Response({
            'is_sharing': False,
            'is_active': False,
            'last_updated': None,
            'session_started': None
        })
