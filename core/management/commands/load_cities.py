import json
from django.core.management.base import BaseCommand
from core.models import City, Province
import os


class Command(BaseCommand):
    help = 'Load provinces and cities from JSON file into the database'

    def handle(self, *args, **kwargs):
        # Load the JSON data
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Build the full path to the JSON file
        file_path = os.path.join(script_dir, 'updated_cities.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            for item in data:
                # Access the province information
                province_data = item['province']
                province_name = province_data['name']

                # Get or create the province
                province, created = Province.objects.get_or_create(
                    name=province_name
                )

                # Iterate through the cities and create City instances
                cities = province_data['cities']
                for city_data in cities:
                    city_name = city_data['name']
                    City.objects.get_or_create(
                        name=city_name, province=province
                    )

        self.stdout.write(self.style.SUCCESS(
            'Successfully populated provinces and cities'))
