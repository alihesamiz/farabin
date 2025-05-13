from pathlib import Path
import json

from django.core.management import BaseCommand
from django.db import transaction

from finance.models import Inflation


class Command(BaseCommand):
    help = "Command to load the existing infalation values to database"
    path: Path = Path(__file__).resolve().parent / "fixtures" / "inflation_table.json"

    def handle(self, *args, **options):
        self.__load_infaltion_values()

    def __load_infaltion_values(self):
        self.stdout.write(self.style.WARNING("Resolving file path... Be Patient!"))
        try:
            values = []
            with transaction.atomic():
                with open(self.path, "r") as file:
                    data = json.load(file)
                    for item in data:
                        db_file = (
                            Inflation.objects.get(year=item["year"])
                            if Inflation.objects.exists()
                            else False
                        )
                        if not db_file:
                            values.append(Inflation(**item))
                        else:
                            self.stdout.write(
                                self.style.ERROR(
                                    f"{item['year']} already exists in database"
                                )
                            )
                values.reverse()
                Inflation.objects.bulk_create(values)
            self.stdout.write(
                self.style.SUCCESS("Successfully saved the fixture ratios")
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"There was an error creating the ratios: {e}")
            )
