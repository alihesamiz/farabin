from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SalesdataConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.salesdata"
    verbose_name = _("Sale Data")
    verbose_name_plural = _("Sales Data")
