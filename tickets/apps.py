from django.utils.translation import gettext_lazy as _
from django.apps import AppConfig

class TicketsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tickets'
    verbose_name = _("Ticket")

    def ready(self):
        import tickets.signals
        