import json
import os


from django.core.management.base import BaseCommand


from core.models import Service


class Command(BaseCommand):
    help = (
        "Load defined services from a JSON if it exists, otherwise from this directory"
    )

    def handle(self, *args, **kwargs):
        script_dir = os.path.dirname(os.path.abspath(__file__))

        file_path = os.path.join(script_dir, "services.json")

        if not os.path.exists(file_path):
            self.stdout.write(
                self.style.ERROR(f"The file '{file_path}' does not exist.")
            )
            return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            self.stdout.write(
                self.style.ERROR(f"Failed to decode JSON from the file '{file_path}'.")
            )
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
            return

        if not data:
            self.stdout.write(
                self.style.WARNING(f"The file '{file_path}' is empty. No data to load.")
            )
            return

        for item in data:

            if all(
                key in item
                for key in ["name", "description", "price", "service_active"]
            ):
                service_name = item["name"]
                service_description = item["description"]
                service_price = item["price"]
                service_active = item["service_active"]

                service, created = Service.objects.get_or_create(
                    name=service_name,
                    defaults={
                        "description": service_description,
                        "price": service_price,
                        "service_active": service_active,
                    },
                )

                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f"Created new service: {service_name}")
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(f"Service already exists: {service_name}")
                    )
            else:
                self.stdout.write(
                    self.style.WARNING(f"Missing required keys in item: {item}")
                )

        self.stdout.write(self.style.SUCCESS("Successfully populated services."))
