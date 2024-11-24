import json
from django.core.management.base import BaseCommand
from company.models import SpecialTech
import os


class Command(BaseCommand):
    help = 'Load special fields from JSON file into the database'

    def handle(self, *args, **kwargs):
        # Load the JSON data

        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Build the full path to the JSON file
        file_path = os.path.join(script_dir, 'special_field.json')

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            # Iterate through the items in the JSON data
            for item in data:
                # Extract the name and create or update the SpecialTech instance
                specialtech_name = item['name']
                SpecialTech.objects.get_or_create(name=specialtech_name)

        self.stdout.write(self.style.SUCCESS(
            'Successfully populated special fields'))
