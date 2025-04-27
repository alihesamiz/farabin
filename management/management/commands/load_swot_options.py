from django.core.management.base import BaseCommand


from management.models import (
    SWOTStrengthOption,
    SWOTWeaknessOption,
    SWOTOpportunityOption,
    SWOTThreatOption,
)


class Command(BaseCommand):
    help = "Load SWOT options from the database"

    def handle(self, *args, **options):
        self._load_swot_options()

    def _load_swot_options(self):
        try:
            from management.models import COMMON_OPPORTUNITY_CHOICES, COMMON_STRENGTH_CHOICES, COMMON_WEAKNESS_CHOICES, COMMON_THREAT_CHOICES

            # Using zip to iterate over the models and their respective choices
            models_choices = zip(
                [SWOTStrengthOption, SWOTWeaknessOption,
                    SWOTOpportunityOption, SWOTThreatOption],

                [COMMON_STRENGTH_CHOICES, COMMON_WEAKNESS_CHOICES,
                    COMMON_OPPORTUNITY_CHOICES,  COMMON_THREAT_CHOICES]
            )

            # Using list comprehension to create instances of the models
            (model.objects.bulk_create([
                model(name=value)
                for value, _ in choices
            ], ignore_conflicts=True) for model, choices in models_choices)

            self.stdout.write(self.style.SUCCESS(
                "SWOT options loaded successfully."))

        except ImportError:

            self.stdout.write(self.style.ERROR(
                "Failed to import SWOT option choices."))
            self.stdout.write(self.style.WARNING(
                "Using common options instead."))

            from management.models import COMMON_SWOT_CHOICES

            # Using zip to iterate over the models and common choices
            for model in [SWOTStrengthOption, SWOTWeaknessOption, SWOTOpportunityOption, SWOTThreatOption]:
                model.objects.bulk_create([
                    model(name=value)
                    for value, _ in COMMON_SWOT_CHOICES
                ])
            self.stdout.write(self.style.SUCCESS(
                "SWOT options loaded successfully."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"An error occurred while loading SWOT options: {str(e)}"))
