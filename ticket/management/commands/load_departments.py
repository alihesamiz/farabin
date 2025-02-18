import logging
import json
import os


from django.core.management.base import BaseCommand


from ticket.models import Department


logger = logging.getLogger("ticket")


class Command(BaseCommand):
    help = 'load defiend services from a json if exists otherwise from this directory'
    logger.info("Starting load-departments command")

    def handle(self, *args, **kwargs):
        script_dir = os.path.dirname(os.path.abspath(__file__))

        file_path = os.path.join(script_dir, 'departments.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            logger.info(f"Found {len(data)} departments in the JSON file")
            for item in data:
                department_name = item['name']
                department_description = item['description']
                service, created = Department.objects.get_or_create(
                    name=department_name,
                    description=department_description,
                )
        logger.info("Finished load-departments command")
        self.stdout.write(self.style.SUCCESS(
            'Successfully populated Departments'))
