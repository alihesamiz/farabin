import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.db import transaction


from company.models import (
    BalanceReport, CompanyService, TaxDeclaration, DiagnosticRequest, CompanyProfile)
from ticket.models import Ticket


logger = logging.getLogger("company")


# TODO: Update the folowing signal handler

@receiver(post_save, sender=TaxDeclaration)
@receiver(post_save, sender=BalanceReport)
def create_diagnostic_request(sender, instance, created, **kwargs):
    """
    Create a DiagnosticRequest if a TaxDeclaration or BalanceReport is sent.
    """

    if instance.is_sent:
        try:
            with transaction.atomic():
                # Get the company and corresponding service
                company = instance.company
                service_instance = CompanyService.objects.select_related('service').filter(
                    company=company,
                    service__name="DIAGNOSTIC",  # Assuming "DIAGNOSTIC" is the service name
                    is_active=True  # Ensure the service is active
                ).first()
                if not service_instance:
                    logger.warning(
                        f"No active 'DIAGNOSTIC' service found for company: {company.id}")
                    return

                # Create the DiagnosticRequest
                DiagnosticRequest.objects.create(
                    company=company,
                    service=service_instance,
                    tax_record=instance if sender is TaxDeclaration else None,
                    balance_record=instance if sender is BalanceReport else None,
                )
                logger.info(
                    f"DiagnosticRequest created for company {company.id}, triggered by {sender.__name__} {instance.id}")

        except Exception as e:
            logger.error(
                f"Error creating DiagnosticRequest for company {company.id}: {e}", exc_info=True)


@receiver(post_save, sender=DiagnosticRequest)
def set_the_file_available(sender, instance, created, **kwargs):
    """
    Signal to handle updates when a DiagnosticRequest's status is changed to 'rejected'.
    """

    if instance.status == DiagnosticRequest.REQUEST_STATUS_REJECTED:
        logger.info(f"DiagnosticRequest {instance.pk} is rejected.")

        # Handle tax record

        if instance.tax_record:
            instance.tax_record.is_sent = False
            instance.tax_record.save()  # Save the change to persist it in the database
            logger.info(
                f"Updated tax_record {instance.tax_record.pk} is_sent to False.")

        # Handle balance record

        if instance.balance_record:
            instance.balance_record.is_sent = False
            instance.balance_record.save()  # Save the change to persist it in the database
            logger.info(
                f"Updated balance_record {instance.balance_record.pk} is_sent to False.")


@receiver(post_save, sender=TaxDeclaration)
@receiver(post_delete, sender=TaxDeclaration)
@receiver(post_save, sender=BalanceReport)
@receiver(post_delete, sender=BalanceReport)
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
