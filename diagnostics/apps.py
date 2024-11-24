from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DiagnosticsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'diagnostics'
    verbose_name = _("Diagnostic")

    def ready(self) -> None:
        import diagnostics.signals
