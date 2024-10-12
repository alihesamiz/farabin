import json
from django.core.management.base import BaseCommand
from diagnostics.models import City, Province


class Command(BaseCommand):
    help = 'Load provinces from JSON file into the database'

    def handle(self, *args, **kwargs):
        # Load the JSON data
        with open('diagnostics/management/commands/provinces.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            for item in data:

                # Get or create the province
                province_name = item['province']
                province, created = Province.objects.get_or_create(
                    name=province_name)

                # Iterate through the cities and create City instances
                cities = item['cities']
                for city_name in cities:
                    City.objects.get_or_create(
                        name=city_name, province=province)

        self.stdout.write(self.style.SUCCESS(
            'Successfully populated cities and province'))
