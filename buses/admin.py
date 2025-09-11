from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.utils.html import format_html
from .models import BusRoute, BusSchedule, GlobalSettings, Stopage


class StopageInline(admin.TabularInline):
    model = Stopage
    extra = 1
    fields = ('name', 'pickup_time', 'drop_time')
    show_change_link = True
    verbose_name = "Stopage"
    verbose_name_plural = "Stopages"

class BusRouteAdmin(admin.ModelAdmin):
    list_display = ('bus_number', 'destination')
    search_fields = ('bus_number', 'destination')
    inlines = [StopageInline]

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
custom_admin_site.register(GlobalSettings)
custom_admin_site.register(Stopage)