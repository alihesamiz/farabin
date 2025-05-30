from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class PackagesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.packages"
    verbose_name = _("Packages")

    def ready(self):
        pass
