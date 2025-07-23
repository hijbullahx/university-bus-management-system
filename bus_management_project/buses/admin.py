from django.contrib import admin
from .models import BusRoute, BusSchedule

# Register your models here.
admin.site.register(BusRoute)
admin.site.register(BusSchedule)