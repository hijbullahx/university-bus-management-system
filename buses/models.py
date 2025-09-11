from django.db import models

# Model to define a specific bus route (e.g., "Bus 1: Main Campus to City Center")
class BusRoute(models.Model):
    bus_number = models.CharField(max_length=10, unique=True, help_text="e.g., 'Bus 1', 'B-101'")
    destination = models.CharField(max_length=100, help_text="e.g., 'City Center', 'Main Campus'")
    description = models.TextField(blank=True, null=True, help_text="Additional details about the route")

    def __str__(self):
        return f"{self.bus_number} - {self.destination}"

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
        return f"{self.route.bus_number} to {self.route.destination} at {self.departure_time.strftime('%I:%M %p')} ({self.get_route_type_display()})"

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
    drop_time = models.TimeField(help_text="Drop time at this stop")

    class Meta:
        ordering = ['pickup_time']
        unique_together = ('route', 'name')

    def __str__(self):
        return f"{self.name} ({self.route.bus_number})"

class GlobalSettings(models.Model):
    active_route_type = models.CharField(
        max_length=10,
        choices=BusSchedule.ROUTE_TYPE_CHOICES,
        default='REGULAR',
        help_text="Set the globally active schedule type (e.g., REGULAR, EXAM). Only schedules of this type will be primarily displayed."
    )
    # We'll ensure only one instance of this model exists
    class Meta:
        verbose_name_plural = "Global Settings"

    def __str__(self):
        return f"Active Schedule: {self.get_active_route_type_display()}"