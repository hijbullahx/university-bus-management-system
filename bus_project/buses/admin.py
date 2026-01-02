from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.utils.html import format_html
from .models import (BusRoute, BusSchedule, GlobalSettings, Stopage, 
                     BusLocation, IssueReport, Notification, UserProfile, DriverRouteSession)


class StopageInline(admin.TabularInline):
    model = Stopage
    extra = 1
    fields = ('name', 'pickup_time')
    show_change_link = True
    verbose_name = "Stopage"
    verbose_name_plural = "Stopages"


class BusRouteAdmin(admin.ModelAdmin):
    list_display = ('bus_number', 'route', 'is_shuttle')
    search_fields = ('bus_number', 'route')
    list_filter = ('is_shuttle',)
    inlines = [StopageInline]


class BusLocationAdmin(admin.ModelAdmin):
    list_display = ('bus', 'driver', 'latitude', 'longitude', 'timestamp', 'is_active', 'is_simulated')
    list_filter = ('is_active', 'is_simulated', 'timestamp')
    search_fields = ('bus__bus_number', 'driver__username')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)


class IssueReportAdmin(admin.ModelAdmin):
    list_display = ('bus', 'driver', 'issue_type', 'status', 'timestamp')
    list_filter = ('issue_type', 'status', 'timestamp')
    search_fields = ('bus__bus_number', 'driver__username', 'description')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'notification_type', 'priority', 'is_active', 'created_at')
    list_filter = ('notification_type', 'priority', 'is_active', 'created_at')
    search_fields = ('title', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-priority', '-created_at')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone_number', 'assigned_bus')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email', 'phone_number')


class DriverRouteSessionAdmin(admin.ModelAdmin):
    list_display = ('driver', 'bus', 'started_at', 'ended_at', 'is_active', 'total_distance')
    list_filter = ('is_active', 'started_at')
    search_fields = ('driver__username', 'bus__bus_number')
    readonly_fields = ('started_at',)
    ordering = ('-started_at',)


class GlobalSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Allow adding only if no instance exists
        if GlobalSettings.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        # Disallow deleting the only instance
        return False
    


# Inject custom CSS for admin branding
class CustomAdminSite(AdminSite):
    site_header = "IUBAT Bus Management Admin"
    site_title = "IUBAT Bus Admin"
    index_title = "Welcome to IUBAT Bus Admin"

    def each_context(self, request):
        context = super().each_context(request)
        context['custom_admin_css'] = 'buses/admin_custom.css'
        return context


custom_admin_site = CustomAdminSite(name='custom_admin')
custom_admin_site.register(BusRoute, BusRouteAdmin)
custom_admin_site.register(BusSchedule)
custom_admin_site.register(GlobalSettings, GlobalSettingsAdmin)
custom_admin_site.register(Stopage)
custom_admin_site.register(BusLocation, BusLocationAdmin)
custom_admin_site.register(IssueReport, IssueReportAdmin)
custom_admin_site.register(Notification, NotificationAdmin)
custom_admin_site.register(UserProfile, UserProfileAdmin)
custom_admin_site.register(DriverRouteSession, DriverRouteSessionAdmin)


# Register with default admin site as well
admin.site.register(BusRoute, BusRouteAdmin)
admin.site.register(BusSchedule)
admin.site.register(GlobalSettings, GlobalSettingsAdmin)
admin.site.register(Stopage)
admin.site.register(BusLocation, BusLocationAdmin)
admin.site.register(IssueReport, IssueReportAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(DriverRouteSession, DriverRouteSessionAdmin)
