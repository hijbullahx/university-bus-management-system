from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django import forms
from django.utils.html import format_html
from .models import (
    BusRoute,
    BusSchedule,
    GlobalSettings,
    Stopage,
    BusLocation,
    IssueReport,
    Notification,
    UserProfile,
    DriverRouteSession,
)


class UserProfileForm(forms.ModelForm):
    """Custom form for UserProfile to conditionally show assigned_bus"""

    class Meta:
        model = UserProfile
        fields = ("role", "phone_number", "assigned_bus")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make assigned_bus field not required by default
        self.fields["assigned_bus"].required = False

        # Hide assigned_bus if role is not DRIVER
        if self.instance.role != "DRIVER":
            self.fields["assigned_bus"].widget = forms.HiddenInput()
        elif self.instance.role == "DRIVER":
            self.fields["assigned_bus"].required = True


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    form = UserProfileForm
    can_delete = False
    fields = ("role", "phone_number", "assigned_bus")
    verbose_name_plural = "User Profile"
    extra = 1  # Changed from 0 to 1 to always show form for new users

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs


class CustomUserAdmin(BaseUserAdmin):
    """Enhanced User Admin with UserProfile inline for creating Drivers and Users"""

    inlines = (UserProfileInline,)

    list_display = (
        "username",
        "email",
        "get_role",
        "first_name",
        "last_name",
        "is_active",
    )
    list_filter = ("profile__role", "is_staff", "is_active", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)

    class Media:
        css = {"all": ("admin/css/custom_admin.css",)}

    def get_role(self, obj):
        """Display user role with emoji"""
        try:
            role = obj.profile.role
            if role == "DRIVER":
                return "🚗 Driver"
            elif role == "USER":
                return "👤 User"
            else:
                return role
        except:
            return "⚠️ No Role"

    get_role.short_description = "Role"

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        """Override to pre-select role from query param"""
        extra_context = extra_context or {}
        if object_id is None and "role" in request.GET:
            # Pre-select role when creating new user
            role = request.GET.get("role")
            if role in ["USER", "DRIVER"]:
                extra_context["default_role"] = role
        return super().changeform_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Ensure UserProfile exists
        if not hasattr(obj, "profile"):
            # Check if role was specified in query params
            role = request.GET.get("role", "USER")
            if role not in ["USER", "DRIVER"]:
                role = "USER"
            UserProfile.objects.create(user=obj, role=role)

    def save_formset(self, request, form, formset, change):
        super().save_formset(request, form, formset, change)


class StopageInline(admin.TabularInline):
    model = Stopage
    extra = 1
    fields = ("name", "pickup_time")
    show_change_link = True
    verbose_name = "Stopage"
    verbose_name_plural = "Stopages"


class BusRouteAdmin(admin.ModelAdmin):
    list_display = ("bus_number", "route", "is_shuttle")
    search_fields = ("bus_number", "route")
    list_filter = ("is_shuttle",)
    inlines = [StopageInline]


class BusLocationAdmin(admin.ModelAdmin):
    list_display = (
        "bus",
        "driver",
        "latitude",
        "longitude",
        "timestamp",
        "is_active",
        "is_simulated",
    )
    list_filter = ("is_active", "is_simulated", "timestamp")
    search_fields = ("bus__bus_number", "driver__username")
    readonly_fields = ("timestamp",)
    ordering = ("-timestamp",)


class IssueReportAdmin(admin.ModelAdmin):
    list_display = ("bus", "driver", "issue_type", "status", "timestamp")
    list_filter = ("issue_type", "status", "timestamp")
    search_fields = ("bus__bus_number", "driver__username", "description")
    readonly_fields = ("timestamp",)
    ordering = ("-timestamp",)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "notification_type", "priority", "is_active", "created_at")
    list_filter = ("notification_type", "priority", "is_active", "created_at")
    search_fields = ("title", "message")
    readonly_fields = ("created_at",)
    ordering = ("-priority", "-created_at")


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("username", "role", "phone_number", "assigned_bus")
    list_filter = ("role",)
    search_fields = ("user__username", "user__email", "phone_number")
    readonly_fields = ("user",)

    def username(self, obj):
        return obj.user.username

    username.short_description = "Username"


class DriverRouteSessionAdmin(admin.ModelAdmin):
    list_display = (
        "driver",
        "bus",
        "started_at",
        "ended_at",
        "is_active",
        "total_distance",
    )
    list_filter = ("is_active", "started_at")
    search_fields = ("driver__username", "bus__bus_number")
    readonly_fields = ("started_at",)
    ordering = ("-started_at",)


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
        context["custom_admin_css"] = "buses/admin_custom.css"
        return context

    def index(self, request, extra_context=None):
        """Override index to show custom user creation section"""
        extra_context = extra_context or {}
        # Return the custom template
        return super().index(request, extra_context)


custom_admin_site = CustomAdminSite(name="custom_admin")
custom_admin_site.register(User, CustomUserAdmin)
custom_admin_site.register(BusRoute, BusRouteAdmin)
custom_admin_site.register(BusSchedule)
custom_admin_site.register(GlobalSettings, GlobalSettingsAdmin)
custom_admin_site.register(Stopage)
custom_admin_site.register(BusLocation, BusLocationAdmin)
custom_admin_site.register(IssueReport, IssueReportAdmin)
custom_admin_site.register(Notification, NotificationAdmin)
custom_admin_site.register(UserProfile, UserProfileAdmin)
custom_admin_site.register(DriverRouteSession, DriverRouteSessionAdmin)


# Register with default admin site (for backup)
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

admin.site.register(BusRoute, BusRouteAdmin)
admin.site.register(BusSchedule)
admin.site.register(GlobalSettings, GlobalSettingsAdmin)
admin.site.register(Stopage)
admin.site.register(BusLocation, BusLocationAdmin)
admin.site.register(IssueReport, IssueReportAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(DriverRouteSession, DriverRouteSessionAdmin)
