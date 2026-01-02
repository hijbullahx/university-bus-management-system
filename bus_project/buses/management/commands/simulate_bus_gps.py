"""
GPS Simulation Management Command

This command simulates bus movements along predefined routes when no real drivers are active.
It's useful for testing and demonstration purposes.

Usage:
    python manage.py simulate_bus_gps
    python manage.py simulate_bus_gps --buses 1 2 3
    python manage.py simulate_bus_gps --interval 5
    python manage.py simulate_bus_gps --duration 300

How it works:
1. Checks if there are any active real (non-simulated) bus locations
2. If no real buses are active, starts simulating bus movements
3. For each bus, creates a path based on its stopages (if available)
4. Moves the bus along the path, creating location updates at regular intervals
5. Uses simple linear interpolation between stops to create smooth movement
6. Adds slight random variations to make movement look more realistic

The simulation continues until:
- A real driver starts tracking (detected by checking for non-simulated locations)
- The specified duration is reached (if provided)
- The command is manually stopped (Ctrl+C)
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from buses.models import BusRoute, BusLocation, Stopage
from datetime import timedelta
import time
import random
import math


class Command(BaseCommand):
    help = 'Simulate GPS movements for buses when no real drivers are active'

    def add_arguments(self, parser):
        parser.add_argument(
            '--buses',
            nargs='+',
            type=int,
            help='Specific bus IDs to simulate (default: all buses)',
        )
        parser.add_argument(
            '--interval',
            type=int,
            default=10,
            help='Update interval in seconds (default: 10)',
        )
        parser.add_argument(
            '--duration',
            type=int,
            default=0,
            help='Total simulation duration in seconds (0 = infinite, default: 0)',
        )
        parser.add_argument(
            '--speed',
            type=float,
            default=30.0,
            help='Average bus speed in km/h (default: 30)',
        )

    def handle(self, *args, **options):
        interval = options['interval']
        duration = options['duration']
        speed_kmh = options['speed']
        bus_ids = options['buses']
        
        self.stdout.write(self.style.SUCCESS('🚌 Starting GPS Simulation System...'))
        
        # Get buses to simulate
        if bus_ids:
            buses = BusRoute.objects.filter(id__in=bus_ids)
        else:
            buses = BusRoute.objects.all()
        
        if not buses.exists():
            self.stdout.write(self.style.ERROR('No buses found to simulate'))
            return
        
        self.stdout.write(f'Simulating {buses.count()} buses')
        self.stdout.write(f'Update interval: {interval} seconds')
        self.stdout.write(f'Speed: {speed_kmh} km/h')
        
        # Initialize simulation state for each bus
        bus_states = {}
        for bus in buses:
            bus_states[bus.id] = self.initialize_bus_state(bus, speed_kmh)
        
        start_time = timezone.now()
        iteration = 0
        
        try:
            while True:
                iteration += 1
                current_time = timezone.now()
                
                # Check if duration limit reached
                if duration > 0:
                    elapsed = (current_time - start_time).total_seconds()
                    if elapsed >= duration:
                        self.stdout.write(self.style.SUCCESS('Duration limit reached. Stopping simulation.'))
                        break
                
                # Check if real drivers are active (non-simulated locations in last 5 minutes)
                recent_time = current_time - timedelta(minutes=5)
                real_active = BusLocation.objects.filter(
                    is_active=True,
                    is_simulated=False,
                    timestamp__gte=recent_time
                ).exists()
                
                if real_active:
                    self.stdout.write(self.style.WARNING('Real driver detected! Pausing simulation...'))
                    # Mark all simulated locations as inactive
                    BusLocation.objects.filter(is_simulated=True, is_active=True).update(is_active=False)
                    time.sleep(interval)
                    continue
                
                # Update each bus
                for bus_id, state in bus_states.items():
                    self.update_bus_position(bus_id, state)
                
                self.stdout.write(f'Iteration {iteration}: Updated {len(bus_states)} buses at {current_time.strftime("%H:%M:%S")}')
                
                # Wait for next update
                time.sleep(interval)
                
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('\n⚠️  Simulation stopped by user'))
        
        # Cleanup: mark all simulated locations as inactive
        BusLocation.objects.filter(is_simulated=True, is_active=True).update(is_active=False)
        self.stdout.write(self.style.SUCCESS('✓ Simulation ended. All simulated locations marked as inactive.'))

    def initialize_bus_state(self, bus, speed_kmh):
        """
        Initialize the state for a bus simulation
        Creates a route path based on stopages or default coordinates
        """
        # Try to get stopages for this route
        stopages = list(bus.stopages.all().order_by('pickup_time'))
        
        if stopages and len(stopages) >= 2:
            # Create path from stopages
            # For now, we'll use dummy coordinates in a line
            # In production, you'd have real lat/lng for each stopage
            path = self.create_path_from_stopages(stopages)
        else:
            # Create a default circular path for demonstration
            path = self.create_default_path()
        
        return {
            'bus': bus,
            'path': path,
            'current_index': 0,
            'progress': 0.0,  # Progress between current and next point (0.0 to 1.0)
            'speed_kmh': speed_kmh,
            'last_update': timezone.now(),
        }

    def create_path_from_stopages(self, stopages):
        """
        Create a path with dummy coordinates for demonstration
        In production, each Stopage would have lat/lng fields
        """
        # IUBAT approximate location: 23.8859° N, 90.3971° E
        base_lat = 23.8859
        base_lng = 90.3971
        
        path = []
        for i, stopage in enumerate(stopages):
            # Create points in a roughly circular pattern
            angle = (i / len(stopages)) * 2 * math.pi
            lat = base_lat + 0.02 * math.cos(angle)
            lng = base_lng + 0.02 * math.sin(angle)
            path.append({'lat': lat, 'lng': lng, 'name': stopage.name})
        
        # Add first point again to complete the loop
        if path:
            path.append(path[0].copy())
        
        return path

    def create_default_path(self):
        """
        Create a default circular path around IUBAT
        """
        base_lat = 23.8859
        base_lng = 90.3971
        num_points = 8
        
        path = []
        for i in range(num_points + 1):
            angle = (i / num_points) * 2 * math.pi
            lat = base_lat + 0.015 * math.cos(angle)
            lng = base_lng + 0.015 * math.sin(angle)
            path.append({'lat': lat, 'lng': lng, 'name': f'Point {i+1}'})
        
        return path

    def update_bus_position(self, bus_id, state):
        """
        Update the position of a bus along its path
        """
        bus = state['bus']
        path = state['path']
        
        if len(path) < 2:
            return
        
        # Calculate how far the bus should move based on time elapsed
        current_time = timezone.now()
        time_diff = (current_time - state['last_update']).total_seconds()
        
        # Calculate distance to move (speed in km/h to degrees approximately)
        # 1 degree ≈ 111 km, so km to degrees = km / 111
        distance_km = (state['speed_kmh'] / 3600) * time_diff
        distance_degrees = distance_km / 111.0
        
        # Get current and next waypoint
        current_idx = state['current_index']
        next_idx = (current_idx + 1) % len(path)
        
        current_point = path[current_idx]
        next_point = path[next_idx]
        
        # Calculate distance between current and next point
        segment_distance = self.calculate_distance(
            current_point['lat'], current_point['lng'],
            next_point['lat'], next_point['lng']
        )
        
        # Update progress
        if segment_distance > 0:
            progress_increment = distance_degrees / segment_distance
            state['progress'] += progress_increment
        
        # Check if we've reached the next waypoint
        if state['progress'] >= 1.0:
            state['current_index'] = next_idx
            state['progress'] = 0.0
            current_idx = state['current_index']
            next_idx = (current_idx + 1) % len(path)
            current_point = path[current_idx]
            next_point = path[next_idx]
        
        # Interpolate position
        progress = min(state['progress'], 1.0)
        lat = current_point['lat'] + (next_point['lat'] - current_point['lat']) * progress
        lng = current_point['lng'] + (next_point['lng'] - current_point['lng']) * progress
        
        # Add small random variation for realism
        lat += random.uniform(-0.0001, 0.0001)
        lng += random.uniform(-0.0001, 0.0001)
        
        # Calculate current speed with some variation
        speed = state['speed_kmh'] * random.uniform(0.8, 1.2)
        
        # Create location update
        BusLocation.objects.create(
            bus=bus,
            driver=None,
            latitude=lat,
            longitude=lng,
            speed=speed,
            is_active=True,
            is_simulated=True
        )
        
        state['last_update'] = current_time

    def calculate_distance(self, lat1, lng1, lat2, lng2):
        """
        Calculate simple Euclidean distance (good enough for small distances)
        """
        return math.sqrt((lat2 - lat1)**2 + (lng2 - lng1)**2)
