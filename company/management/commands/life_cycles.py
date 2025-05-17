from decimal import Decimal, InvalidOperation
from pathlib import Path
import json

from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand

from company.models import LifeCycleFeature, LifeCycleFinancialResource


class Command(BaseCommand):
    help = "Loads the default features and cpm values"
    path = Path(__file__).resolve().parent / "fixtures" / "life_cycle_features.json"

    def handle(self, *args, **options):
        self.__load_features()
        self.__load_capital_providing_values()

    def __load_capital_providing_values(self):
        self.stdout.write(self.style.WARNING("Resolving method values..."))
        for code, name in LifeCycleFinancialResource.RESOURCE_TYPES:
            if not LifeCycleFinancialResource.objects.filter(name=code).exists():
                LifeCycleFinancialResource.objects.create(name=code)
                self.stdout.write(self.style.SUCCESS(f"Successfully added: {name}"))
            else:
                self.stdout.write(self.style.WARNING(f"{name} already exists."))

        self.stdout.write(self.style.SUCCESS("Resource loading complete."))

    def __load_features(self):
        self.stdout.write(self.style.WARNING("Resolving features..."))
        features = []
        try:
            with open(self.path, "r") as file:
                data = json.load(file)
                for feature in data:
                    try:
                        LifeCycleFeature.objects.get(name=feature["name"])
                        self.stdout.write(
                            self.style.ERROR(
                                f"Feature with name '{feature['name']}' already exists"
                            )
                        )
                    except ObjectDoesNotExist:
                        try:
                            weight = Decimal(feature["weight"])
                            features.append(
                                LifeCycleFeature(name=feature["name"], weight=weight)
                            )
                        except (InvalidOperation, ValueError):
                            self.stdout.write(
                                self.style.ERROR(
                                    f"Invalid weight value for feature '{feature['name']}': {feature['weight']}"
                                )
                            )

            if features:
                LifeCycleFeature.objects.bulk_create(features)
                self.stdout.write(self.style.SUCCESS("Features loaded successfully"))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("File not found"))

        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR("Invalid JSON"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error appeared: {e}"))
