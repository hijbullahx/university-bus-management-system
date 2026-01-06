from django.db import models
from accounts.models import User
from schedules.models import Route

class Notification(models.Model):
    PRIORITY_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('danger', 'Urgent'),
        ('success', 'Success'),
    ]

    TARGET_CHOICES = [
        ('all', 'All Users'),
        ('users', 'Students/Faculty/Staff'),
        ('drivers', 'All Drivers'),
        ('route', 'Specific Route'),
    ]

    title = models.CharField(max_length=200)
    message = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='info')
    target = models.CharField(max_length=20, choices=TARGET_CHOICES, default='all')
    target_route = models.ForeignKey(Route, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_notifications')
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class UserNotification(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='user_notifications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_received')
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'user_notifications'
        unique_together = ['notification', 'user']

    def __str__(self):
        return f"{self.notification.title} - {self.user.username}"
