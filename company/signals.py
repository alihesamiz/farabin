import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache


from finance.models import TaxDeclarationFile, BalanceReportFile
from company.models import CompanyProfile
from ticket.models import Ticket


logger = logging.getLogger("company")


@receiver(post_save, sender=TaxDeclarationFile)
@receiver(post_delete, sender=TaxDeclarationFile)
@receiver(post_save, sender=BalanceReportFile)
@receiver(post_delete, sender=BalanceReportFile)
def clear_dashboard_cache(sender, instance, **kwargs):
    """
    Signal to clear the cache when a Service instance is updated.
    """
    cache_key = f"dashboard_data_{instance.company.user.id}"
    cache.delete(cache_key)
    logger.info(
        f"Cleared dashboard cache for user {instance.company.user.id} due to {sender.__name__} {instance.id} update.")


@receiver(post_save, sender=Ticket)
@receiver(post_delete, sender=Ticket)
def clear_dashboard_cache(sender, instance, **kwargs):
    """
    Signal to clear the cache when a Service instance is updated.
    """
    cache_key = f"dashboard_data_{instance.issuer.user.id}"
    cache.delete(cache_key)
    logger.info(
        f"Cleared dashboard cache for user {instance.issuer.user.id} due to Ticket {instance.id} update.")


@receiver(post_save, sender=CompanyProfile)
def clear_profile_cache(sender, instance, **kwargs):
    """
    Signal to clear the cache when a CompanyProfile instance is updated.
    """
    cache_key = f"company_profile_{instance.user.id}"
    cache.delete(cache_key)
    logger.info(f"Cleared company profile cache for user {instance.user.id}.")
