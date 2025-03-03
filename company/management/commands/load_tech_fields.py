import logging
import json
import os


from django.core.management.base import BaseCommand


from company.models import TechField


logger = logging.getLogger("company")


class Command(BaseCommand):
    help = 'Load tech fields from JSON file into the database'

    def handle(self, *args, **kwargs):

        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            logging.info("Loading Tech Field JSON file")
            file_path = os.path.join(script_dir, 'tech_field.json')

            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

                for item in data:
                    tech_name = item['name']
                    TechField.objects.get_or_create(name=tech_name)
            logging.info("TechField model loaded successfully")
        except Exception as e:
            logging.error(f"Error while loading tech fields: {e}")
