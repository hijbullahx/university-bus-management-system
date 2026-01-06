from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Create superuser from environment variables if none exists'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin12345'
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
            return
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            user_type='admin',
            approval_status='approved'
        )
        self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully'))
