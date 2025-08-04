from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SwotConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.swot"
    verbose_name = _("SWOT")
