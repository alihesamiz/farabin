import logging

from django.core.management import BaseCommand

from apps.company.models import LifeCycle


logger = logging.getLogger("company")


class Command(BaseCommand):
    help = "This command loads the different capital providing methods"

    def handle(self, *args, **kwargs):
        try:
            logging.info("Loading capital providing methods ...")
            for choice, _ in LifeCycle.LIFE_CYCLE_CHOICES:
                LifeCycle.objects.get_or_create(capital_providing=choice)

            logging.info("Capital providing methods loaded successfully.")

        except Exception as e:
            logging.error(f"Error loading capital providing methods: {e}")
