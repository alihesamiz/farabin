from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import BalanceReport, CompanyProfile, CompanyService, TaxDeclaration, DiagnosticRequest
from .tasks import send_file_uploading_notification


@receiver(post_save, sender=TaxDeclaration)
@receiver(post_save, sender=BalanceReport)
def create_request_if_sent(sender, instance, created, **kwargs):
    if instance.is_sent:
        try:
            service_instance = CompanyService.objects.get(name="DIAGNOSTIC")
        except CompanyService.DoesNotExist:
            return
        DiagnosticRequest.objects.create(
            company=instance.company,
            service=service_instance,
            tax_record=instance if sender is TaxDeclaration else None,  # Assign service if needed
            # Assign service if needed
            balance_record=instance if sender is BalanceReport else None,
        )
        send_file_uploading_notification.delay(
            'tax' if sender is TaxDeclaration else 'balancereport'
        )

