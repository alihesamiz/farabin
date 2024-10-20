import json
from django.core.management.base import BaseCommand
from core.models import Province


class Command(BaseCommand):
    help = 'Load provinces from JSON file into the database'

    def handle(self, *args, **kwargs):
        # Path to your JSON file
        with open('core/management/commands/provinces.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

            for item in data:
                province_name = item['province']
                # Create or get province by name
                Province.objects.get_or_create(name=province_name)

        self.stdout.write(self.style.SUCCESS('Successfully loaded provinces!'))
