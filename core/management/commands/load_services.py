import json
import os
from django.core.management.base import BaseCommand
from core.models import Service


class Command(BaseCommand):
    help = 'load defiend services from a json if exists otherwise from this directory'

    def handle(self, *args, **kwargs):
        # Load the JSON data
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Build the full path to the JSON file
        file_path = os.path.join(script_dir, 'services.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            for item in data:
                # Access the province information
                service_name = item['name']
                service_description = item['description']
                service_price = item['price']
                service_active = item['service_active']
                # Get or create the province
                service, created = Service.objects.get_or_create(
                    name=service_name,
                    description=service_description,
                    price=service_price,
                    service_active=service_active,
                )

        self.stdout.write(self.style.SUCCESS(
            'Successfully populated Services'))
