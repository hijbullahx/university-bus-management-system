from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Create default superusers and authority users for Render deployment.'

    def handle(self, *args, **options):
        # Admin superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',
                role='admin',
                is_active=True,
                approval_status='approved'
            )
            self.stdout.write(self.style.SUCCESS('Created admin: admin/admin123'))
        else:
            self.stdout.write('Admin user already exists.')

        # Authority user
        if not User.objects.filter(username='authority').exists():
            User.objects.create_user(
                username='authority',
                email='authority@example.com',
                password='authority123',
                role='authority',
                is_active=True,
                approval_status='approved'
            )
            self.stdout.write(self.style.SUCCESS('Created authority: authority/authority123'))
        else:
            self.stdout.write('Authority user already exists.')
