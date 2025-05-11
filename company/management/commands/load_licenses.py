import logging

from django.core.management import BaseCommand

from company.models import License


logger = logging.getLogger("company")


class Command(BaseCommand):
    help = "This command will load up the licenses types"

    def handle(self, *args, **kwargs):
        TYPES = {
            "tl": "فناور",
            "kbl": "دانش بنیان",
            "ol": "سایر",
            "itl": "عضو شهرک صنعتی",
        }
        logger.info("Loading licenses types...")

        try:
            for code, name in TYPES.items():
                license, created = License.objects.update_or_create(
                    code=code, defaults={"name": name}
                )
            logger.info("Licenses types loaded successfully")
        except Exception as e:
            logger.error(f"Error while Loading licenses types:{e}")
