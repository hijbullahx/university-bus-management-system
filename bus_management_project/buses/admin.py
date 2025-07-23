from django.contrib import admin
from .models import BusRoute, BusSchedule, GlobalSettings 


class GlobalSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Allow adding only if no instance exists
        if GlobalSettings.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Disallow deleting the only instance
        return False
    

admin.site.register(BusRoute)
admin.site.register(BusSchedule)
admin.site.register(GlobalSettings)