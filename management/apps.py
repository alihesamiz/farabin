from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig


class ManagementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "management"
    verbose_name = _("Management")

    def ready(self):
        import management.signals
