from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Create superuser from environment variables if none exists'

    def handle(self, *args, **options):
        User = get_user_model()
        
        username = os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
        
        if not password:
            self.stdout.write(self.style.WARNING('DJANGO_SUPERUSER_PASSWORD not set, skipping superuser creation'))
            return
        
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
