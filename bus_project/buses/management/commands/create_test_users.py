"""
Management command to create test users for all 4 roles
Usage: python manage.py create_test_users
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from buses.models import UserProfile, BusRoute


class Command(BaseCommand):
    help = 'Creates test users for all 4 roles (User, Driver, Admin, Authority)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('\n🚌 IUBAT Bus Management - Creating Test Users\n'))
        
        # Create test users
        users_data = [
            {
                'username': 'testuser',
                'password': 'user123',
                'email': 'user@iubat.edu',
                'first_name': 'Test',
                'last_name': 'User',
                'role': 'USER',
                'phone': '01712345678'
            },
            {
                'username': 'driver1',
                'password': 'driver123',
                'email': 'driver1@iubat.edu',
                'first_name': 'Driver',
                'last_name': 'One',
                'role': 'DRIVER',
                'phone': '01712345679'
            },
            {
                'username': 'driver2',
                'password': 'driver123',
                'email': 'driver2@iubat.edu',
                'first_name': 'Driver',
                'last_name': 'Two',
                'role': 'DRIVER',
                'phone': '01712345680'
            },
            {
                'username': 'admin',
                'password': 'admin123',
                'email': 'admin@iubat.edu',
                'first_name': 'System',
                'last_name': 'Admin',
                'role': 'ADMIN',
                'phone': '01712345681'
            },
            {
                'username': 'authority',
                'password': 'authority123',
                'email': 'authority@iubat.edu',
                'first_name': 'University',
                'last_name': 'Authority',
                'role': 'AUTHORITY',
                'phone': '01712345682'
            },
        ]
        
        # Get first two buses for driver assignment (if they exist)
        buses = list(BusRoute.objects.all()[:2])
        
        created_count = 0
        updated_count = 0
        
        for user_data in users_data:
            username = user_data['username']
            
            # Check if user exists
            user, user_created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            
            # Set password (whether new or existing)
            user.set_password(user_data['password'])
            
            # Set superuser for admin and authority
            if user_data['role'] in ['ADMIN', 'AUTHORITY']:
                user.is_staff = True
                user.is_superuser = True
            
            user.save()
            
            # Create or update profile
            profile, profile_created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'role': user_data['role'],
                    'phone_number': user_data['phone']
                }
            )
            
            if not profile_created:
                profile.role = user_data['role']
                profile.phone_number = user_data['phone']
            
            # Assign buses to drivers
            if user_data['role'] == 'DRIVER' and buses:
                if username == 'driver1' and len(buses) > 0:
                    profile.assigned_bus = buses[0]
                elif username == 'driver2' and len(buses) > 1:
                    profile.assigned_bus = buses[1]
            
            profile.save()
            
            if user_created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created: {username} ({user_data["role"]}) - Password: {user_data["password"]}'
                    )
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f'↻ Updated: {username} ({user_data["role"]}) - Password: {user_data["password"]}'
                    )
                )
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Complete! Created: {created_count}, Updated: {updated_count}'))
        self.stdout.write(self.style.SUCCESS('\n📝 Test User Credentials:\n'))
        self.stdout.write('=' * 70)
        
        for user_data in users_data:
            self.stdout.write(
                f"  {user_data['role']:10} | Username: {user_data['username']:12} | Password: {user_data['password']}"
            )
        
        self.stdout.write('=' * 70)
        self.stdout.write(self.style.SUCCESS('\n🌐 Access URLs:'))
        self.stdout.write('  Login:           http://127.0.0.1:8000/buses/login/')
        self.stdout.write('  User Map:        http://127.0.0.1:8000/buses/map/')
        self.stdout.write('  Driver Dashboard: http://127.0.0.1:8000/buses/driver/')
        self.stdout.write('  Admin Dashboard:  http://127.0.0.1:8000/buses/admin-dashboard/')
        self.stdout.write('\n')
