from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# User Profile Extension for Role Management
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('USER', 'User'),
        ('DRIVER', 'Driver'),
        ('ADMIN', 'Admin'),
        ('AUTHORITY', 'Authority'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    assigned_bus = models.ForeignKey('BusRoute', on_delete=models.SET_NULL, null=True, blank=True, 
                                     help_text="For drivers: which bus they're assigned to")
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


# Model to define a specific bus route (e.g., "Bus 1: Main Campus to City Center")

class BusRoute(models.Model):
    bus_number = models.CharField(max_length=10, unique=True, help_text="e.g., 'Bus 1', 'B-101'")
    route = models.CharField(max_length=100, help_text="e.g., 'City Center', 'Main Campus'")
    ultimate_pickup_time = models.TimeField(blank=True, null=True, help_text="Earliest pick-up time among stopages")
    ultimate_drop_time = models.TimeField(blank=True, null=True, help_text="Latest pick-up time among stopages")
    is_shuttle = models.BooleanField(default=False, help_text="Is this a shuttle bus route?")
    notes = models.TextField(blank=True, null=True, help_text="Extra notes or shuttle schedule data (JSON)")

    def __str__(self):
        return f"{self.bus_number} - {self.route}"

    class Meta:
        verbose_name = "Bus Route"
        verbose_name_plural = "Bus Routes"
        ordering = ['bus_number']


# Model to define specific schedules for a bus route
class BusSchedule(models.Model):
    ROUTE_TYPE_CHOICES = [
        ('REGULAR', 'Regular Schedule'),
        ('EXAM', 'Exam Schedule'),
        ('SPECIAL', 'Special Event Schedule'),
    ]

    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE, related_name='schedules', help_text="The bus route this schedule belongs to")
    departure_time = models.TimeField(help_text="Scheduled departure time")
    arrival_time = models.TimeField(blank=True, null=True, help_text="Scheduled arrival time (optional)")
    is_active = models.BooleanField(default=True, help_text="Is this schedule currently active?")
    route_type = models.CharField(max_length=10, choices=ROUTE_TYPE_CHOICES, default='REGULAR', help_text="Type of schedule (e.g., Regular, Exam)")
    notes = models.TextField(blank=True, null=True, help_text="Any specific notes for this schedule (e.g., 'Runs only on weekdays')")

    def __str__(self):
        return f"{self.route.bus_number} to {self.route.route} at {self.departure_time.strftime('%I:%M %p')} ({self.get_route_type_display()})"

    class Meta:
        verbose_name = "Bus Schedule"
        verbose_name_plural = "Bus Schedules"
        # Ensures that for a given route and type, a departure time is unique
        unique_together = ('route', 'departure_time', 'route_type')
        ordering = ['route__bus_number', 'departure_time']


class Stopage(models.Model):
    route = models.ForeignKey(BusRoute, on_delete=models.CASCADE, related_name='stopages')
    name = models.CharField(max_length=100, help_text="Stopage name (e.g., 'Main Gate', 'Science Building')")
    pickup_time = models.TimeField(help_text="Pick-up time at this stop")

    class Meta:
        ordering = ['pickup_time']
        unique_together = ('route', 'name')

    def __str__(self):
        return f"{self.name} ({self.route.bus_number})"



# Real-time Bus Location Model (GPS Tracking)
class BusLocation(models.Model):
    bus = models.ForeignKey(BusRoute, on_delete=models.CASCADE, related_name='locations')
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                               help_text="Driver who is currently operating this bus")
    latitude = models.FloatField(help_text="Current latitude")
    longitude = models.FloatField(help_text="Current longitude")
    timestamp = models.DateTimeField(default=timezone.now, help_text="Time when location was recorded")
    speed = models.FloatField(default=0.0, help_text="Speed in km/h", blank=True, null=True)
    is_active = models.BooleanField(default=True, help_text="Is the bus currently on route?")
    is_simulated = models.BooleanField(default=False, help_text="Is this a simulated location?")
    
    def __str__(self):
        return f"{self.bus.bus_number} at ({self.latitude}, {self.longitude}) - {self.timestamp.strftime('%I:%M %p')}"
    
    class Meta:
        verbose_name = "Bus Location"
        verbose_name_plural = "Bus Locations"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp', 'bus']),
            models.Index(fields=['is_active']),
        ]


# Issue Report Model (For Drivers to report problems)
class IssueReport(models.Model):
    ISSUE_TYPE_CHOICES = [
        ('BREAKDOWN', 'Mechanical Breakdown'),
        ('TRAFFIC', 'Heavy Traffic'),
        ('EMERGENCY', 'Emergency'),
        ('ACCIDENT', 'Accident'),
        ('OTHER', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]
    
    bus = models.ForeignKey(BusRoute, on_delete=models.CASCADE, related_name='issues')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reported_issues')
    issue_type = models.CharField(max_length=20, choices=ISSUE_TYPE_CHOICES)
    description = models.TextField(help_text="Detailed description of the issue")
    location_lat = models.FloatField(null=True, blank=True)
    location_lng = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                    related_name='resolved_issues')
    
    def __str__(self):
        return f"{self.get_issue_type_display()} - {self.bus.bus_number} by {self.driver.username}"
    
    class Meta:
        verbose_name = "Issue Report"
        verbose_name_plural = "Issue Reports"
        ordering = ['-timestamp']


# Notification Model (For system-wide alerts)
class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ('DELAY', 'Bus Delay'),
        ('CANCELLED', 'Route Cancelled'),
        ('ISSUE', 'Bus Issue'),
        ('ANNOUNCEMENT', 'General Announcement'),
        ('EMERGENCY', 'Emergency Alert'),
    ]
    
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    bus = models.ForeignKey(BusRoute, on_delete=models.CASCADE, null=True, blank=True, 
                           related_name='notifications')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=1, help_text="1=Low, 2=Medium, 3=High")
    
    def __str__(self):
        return f"{self.title} - {self.get_notification_type_display()}"
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-priority', '-created_at']


# Driver Route Session (Track when drivers start/stop routes)
class DriverRouteSession(models.Model):
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='route_sessions')
    bus = models.ForeignKey(BusRoute, on_delete=models.CASCADE, related_name='sessions')
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    total_distance = models.FloatField(default=0.0, help_text="Total distance traveled in km")
    
    def __str__(self):
        return f"{self.driver.username} - {self.bus.bus_number} ({self.started_at.strftime('%Y-%m-%d %I:%M %p')})"
    
    class Meta:
        verbose_name = "Driver Route Session"
        verbose_name_plural = "Driver Route Sessions"
        ordering = ['-started_at']