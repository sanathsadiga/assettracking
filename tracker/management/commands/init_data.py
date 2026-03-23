from django.core.management.base import BaseCommand
from tracker.models import Category, Location


class Command(BaseCommand):
    help = 'Initialize categories and locations'

    def handle(self, *args, **options):
        # Create categories
        categories = [
            ('Laptop', 'Laptop computers'),
            ('Desktop', 'Desktop computers'),
            ('Monitor', 'Computer monitors'),
            ('Keyboard', 'Computer keyboards'),
            ('Mouse', 'Computer mice'),
            ('Printer', 'Network printers'),
            ('Router', 'Network routers'),
            ('Server', 'Server equipment'),
            ('Mobile Device', 'Mobile devices and tablets'),
            ('Other', 'Other equipment'),
        ]

        for name, desc in categories:
            obj, created = Category.objects.get_or_create(
                name=name, 
                defaults={'description': desc}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {name}')
                )

        # Create locations
        locations = [
            ('Office - Building A', 'Office in Building A'),
            ('Office - Building B', 'Office in Building B'),
            ('Warehouse', 'Main warehouse'),
            ('Conference Room 1', 'Conference room 1'),
            ('Conference Room 2', 'Conference room 2'),
            ('Break Room', 'Break room and kitchen'),
            ('IT Department', 'IT department office'),
            ('Reception', 'Reception area'),
            ('Storage', 'Storage area'),
            ('In Transit', 'Items in transit'),
        ]

        for name, desc in locations:
            obj, created = Location.objects.get_or_create(
                name=name,
                defaults={'description': desc}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created location: {name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\nTotal categories: {Category.objects.count()}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total locations: {Location.objects.count()}')
        )
