from django.urls import path
from . import api_views

urlpatterns = [
    path('notifications/', api_views.notification_list_api, name='api_notification_list'),
    path('notifications/user/', api_views.user_notifications_api, name='api_user_notifications'),
    path('notifications/unread/', api_views.unread_notifications_api, name='api_unread_notifications'),
    path('notifications/<int:pk>/read/', api_views.mark_read_api, name='api_mark_read'),
    path('notifications/read-all/', api_views.mark_all_read_api, name='api_mark_all_read'),
    path('notifications/unread-count/', api_views.unread_count_api, name='api_unread_count'),
]
