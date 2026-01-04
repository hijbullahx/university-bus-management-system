from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views, views_admin
from . import views_auth, views_home
from . import (
    views_admin_route,
    views_admin_route_edit,
    views_route_stopages,
    views_admin_shuttle,
    views_admin_shuttle_edit,
)
from . import views_user_map, views_driver, views_admin_dashboard

app_name = "buses"  # Define the app namespace

urlpatterns = [
    # Authentication - Unified Login System
    path("login/", views_auth.unified_login, name="login"),
    path("logout/", views_auth.custom_logout, name="logout"),
    # User Panel - Public-facing routes
    path("user/", include("buses.user_panel.urls", namespace="user_panel")),
    # Legacy routes (keeping for backward compatibility)
    path("", views_home.home_view, name="home"),
    path("home/", views_home.home_view, name="home"),
    path("map/", views_user_map.user_map_view, name="user_map"),
    path("schedules/", views.bus_schedule_list, name="bus_schedule_list"),
    # Driver routes
    path("driver/", views_driver.driver_dashboard, name="driver_dashboard"),
    path(
        "driver/start-route/",
        views_driver.driver_start_route,
        name="driver_start_route",
    ),
    path("driver/tracking/", views_driver.driver_tracking, name="driver_tracking"),
    path("driver/end-route/", views_driver.driver_end_route, name="driver_end_route"),
    path(
        "driver/report-issue/",
        views_driver.driver_report_issue,
        name="driver_report_issue",
    ),
    path("driver/schedules/", views_driver.driver_schedules, name="driver_schedules"),
    # Admin/Authority routes
    path(
        "admin-dashboard/",
        views_admin_dashboard.admin_dashboard,
        name="admin_dashboard",
    ),
    path(
        "admin-dashboard/reports/",
        views_admin_dashboard.admin_reports,
        name="admin_reports",
    ),
    path(
        "admin-dashboard/live-tracking/",
        views_admin_dashboard.admin_live_tracking,
        name="admin_live_tracking",
    ),
    path(
        "admin-dashboard/manage-issues/",
        views_admin_dashboard.admin_manage_issues,
        name="admin_manage_issues",
    ),
    path(
        "admin-dashboard/manage-notifications/",
        views_admin_dashboard.admin_manage_notifications,
        name="admin_manage_notifications",
    ),
    path(
        "route/<int:route_id>/stopages/",
        views_route_stopages.route_stopages_detail,
        name="route_stopages_detail",
    ),
]
