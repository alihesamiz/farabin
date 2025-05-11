import logging
import json
import os


from django.core.management.base import BaseCommand


from company.models import SpecialTech


logger = logging.getLogger("company")


class Command(BaseCommand):
    help = "Load special fields from JSON file into the database"

    def handle(self, *args, **kwargs):
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            logger.info("Loading JSON file")
            file_path = os.path.join(script_dir, "special_field.json")

            logger.info("Populating SpecialTech model")
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

                for item in data:
                    specialtech_name = item["name"]
                    SpecialTech.objects.get_or_create(name=specialtech_name)
            logger.info("SpecialTech model loaded")
        except Exception as e:
            logger.error(f"Error while loading special fields: {e}")
