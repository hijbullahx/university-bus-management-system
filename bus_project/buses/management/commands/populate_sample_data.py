"""
Management command to populate the database with sample bus routes and schedules
Usage: python manage.py populate_sample_data
"""
from django.core.management.base import BaseCommand
from buses.models import BusRoute, BusSchedule, Stopage
from datetime import time


class Command(BaseCommand):
    help = 'Populates the database with sample bus routes, schedules, and stopages'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('\n🚌 Populating Sample Bus Data\n'))
        
        # Sample bus routes
        routes_data = [
            {
                'bus_number': 'Bus-001',
                'route': 'Main Campus to City Center',
                'ultimate_pickup_time': time(7, 0),
                'ultimate_drop_time': time(9, 0),
                'is_shuttle': False,
                'stopages': [
                    {'name': 'IUBAT Main Gate', 'time': time(7, 0)},
                    {'name': 'Bashundhara R/A', 'time': time(7, 15)},
                    {'name': 'Kuril Flyover', 'time': time(7, 30)},
                    {'name': 'Rampura Bridge', 'time': time(7, 45)},
                    {'name': 'Mouchak', 'time': time(8, 0)},
                    {'name': 'Farmgate', 'time': time(8, 20)},
                    {'name': 'Karwan Bazar', 'time': time(8, 35)},
                    {'name': 'Shahbag', 'time': time(8, 50)},
                ],
                'schedules': [
                    {'departure': time(7, 0), 'arrival': time(9, 0), 'type': 'REGULAR'},
                    {'departure': time(13, 0), 'arrival': time(15, 0), 'type': 'REGULAR'},
                    {'departure': time(17, 0), 'arrival': time(19, 0), 'type': 'REGULAR'},
                ]
            },
            {
                'bus_number': 'Bus-002',
                'route': 'Main Campus to Uttara',
                'ultimate_pickup_time': time(7, 30),
                'ultimate_drop_time': time(9, 30),
                'is_shuttle': False,
                'stopages': [
                    {'name': 'IUBAT Main Gate', 'time': time(7, 30)},
                    {'name': 'Jamuna Future Park', 'time': time(7, 50)},
                    {'name': 'House Building', 'time': time(8, 10)},
                    {'name': 'Azampur', 'time': time(8, 25)},
                    {'name': 'Uttara Sector 7', 'time': time(8, 40)},
                    {'name': 'Uttara Sector 10', 'time': time(9, 0)},
                    {'name': 'Airport', 'time': time(9, 20)},
                ],
                'schedules': [
                    {'departure': time(7, 30), 'arrival': time(9, 30), 'type': 'REGULAR'},
                    {'departure': time(14, 0), 'arrival': time(16, 0), 'type': 'REGULAR'},
                    {'departure': time(18, 0), 'arrival': time(20, 0), 'type': 'REGULAR'},
                ]
            },
            {
                'bus_number': 'Shuttle-A',
                'route': 'Campus Shuttle Loop',
                'ultimate_pickup_time': time(8, 0),
                'ultimate_drop_time': time(17, 0),
                'is_shuttle': True,
                'notes': 'Runs every 30 minutes during class hours',
                'stopages': [
                    {'name': 'Admin Building', 'time': time(8, 0)},
                    {'name': 'Engineering Block', 'time': time(8, 5)},
                    {'name': 'Business Faculty', 'time': time(8, 10)},
                    {'name': 'Student Center', 'time': time(8, 15)},
                    {'name': 'Library', 'time': time(8, 20)},
                    {'name': 'Sports Complex', 'time': time(8, 25)},
                ],
                'schedules': [
                    {'departure': time(8, 0), 'arrival': time(8, 30), 'type': 'REGULAR'},
                    {'departure': time(9, 0), 'arrival': time(9, 30), 'type': 'REGULAR'},
                    {'departure': time(10, 0), 'arrival': time(10, 30), 'type': 'REGULAR'},
                    {'departure': time(11, 0), 'arrival': time(11, 30), 'type': 'REGULAR'},
                    {'departure': time(12, 0), 'arrival': time(12, 30), 'type': 'REGULAR'},
                    {'departure': time(13, 0), 'arrival': time(13, 30), 'type': 'REGULAR'},
                    {'departure': time(14, 0), 'arrival': time(14, 30), 'type': 'REGULAR'},
                    {'departure': time(15, 0), 'arrival': time(15, 30), 'type': 'REGULAR'},
                    {'departure': time(16, 0), 'arrival': time(16, 30), 'type': 'REGULAR'},
                ]
            },
        ]
        
        created_routes = 0
        created_stopages = 0
        created_schedules = 0
        
        for route_data in routes_data:
            # Create or get route
            route, route_created = BusRoute.objects.get_or_create(
                bus_number=route_data['bus_number'],
                defaults={
                    'route': route_data['route'],
                    'ultimate_pickup_time': route_data['ultimate_pickup_time'],
                    'ultimate_drop_time': route_data['ultimate_drop_time'],
                    'is_shuttle': route_data['is_shuttle'],
                    'notes': route_data.get('notes', '')
                }
            )
            
            if route_created:
                created_routes += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created route: {route.bus_number}'))
            else:
                self.stdout.write(self.style.WARNING(f'↻ Route exists: {route.bus_number}'))
            
            # Create stopages
            for stopage_data in route_data['stopages']:
                stopage, stopage_created = Stopage.objects.get_or_create(
                    route=route,
                    name=stopage_data['name'],
                    defaults={'pickup_time': stopage_data['time']}
                )
                if stopage_created:
                    created_stopages += 1
            
            # Create schedules
            for schedule_data in route_data['schedules']:
                schedule, schedule_created = BusSchedule.objects.get_or_create(
                    route=route,
                    departure_time=schedule_data['departure'],
                    route_type=schedule_data['type'],
                    defaults={
                        'arrival_time': schedule_data['arrival'],
                        'is_active': True
                    }
                )
                if schedule_created:
                    created_schedules += 1
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Complete!'))
        self.stdout.write(self.style.SUCCESS(f'   Routes: {created_routes}'))
        self.stdout.write(self.style.SUCCESS(f'   Stopages: {created_stopages}'))
        self.stdout.write(self.style.SUCCESS(f'   Schedules: {created_schedules}\n'))
