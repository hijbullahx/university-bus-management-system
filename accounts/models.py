from django.db.models.signals import post_migrate
from django.dispatch import receiver

# Automatically create default admin and authority users after migrations (for Render, free tier)
@receiver(post_migrate)
def create_default_users(sender, **kwargs):
    from accounts.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            role='admin',
            is_active=True,
            approval_status='approved'
        )
    if not User.objects.filter(username='authority').exists():
        User.objects.create_user(
            username='authority',
            email='authority@example.com',
            password='authority123',
            role='authority',
            is_active=True,
            approval_status='approved'
        )
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('staff', 'Staff'),
        ('driver', 'Driver'),
        ('admin', 'Admin'),
        ('authority', 'Authority'),
    ]
    
    APPROVAL_STATUS = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True, help_text='Full address')
    nid_number = models.CharField(max_length=50, blank=True, help_text='National ID Number')
    employee_id = models.CharField(max_length=50, blank=True)
    university_id = models.CharField(max_length=50, blank=True, help_text='University ID for verification')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_active_driver = models.BooleanField(default=False)
    approval_status = models.CharField(max_length=20, choices=APPROVAL_STATUS, default='pending')
    approved_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_users')
    approved_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_student(self):
        return self.role == 'student'

    @property
    def is_faculty(self):
        return self.role == 'faculty'

    @property
    def is_staff_member(self):
        return self.role == 'staff'

    @property
    def is_driver(self):
        return self.role == 'driver'

    @property
    def is_admin_user(self):
        return self.role == 'admin'

    @property
    def is_authority(self):
        return self.role == 'authority'

    @property
    def is_regular_user(self):
        return self.role in ['student', 'faculty', 'staff']

    @property
    def is_approved(self):
        return self.approval_status == 'approved'

    @property
    def is_pending(self):
        return self.approval_status == 'pending'


class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver_profile')
    license_number = models.CharField(max_length=50)
    license_expiry = models.DateField()
    emergency_contact = models.CharField(max_length=20)
    years_experience = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    current_shift_start = models.TimeField(null=True, blank=True)
    current_shift_end = models.TimeField(null=True, blank=True)

    class Meta:
        db_table = 'driver_profiles'

    def __str__(self):
        return f"Driver: {self.user.get_full_name() or self.user.username}"
