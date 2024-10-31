import time
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import FinancialAsset
from .tasks import perform_calculations
from celery.result import AsyncResult

# Trigger task after FinancialAsset is saved or deleted


@receiver([post_save, post_delete], sender=FinancialAsset)
def trigger_calculation_task(sender, instance, **kwargs):
    # Collect all related financial asset IDs for the company
    financial_asset_ids = FinancialAsset.objects.filter(
        company=instance.company
    ).order_by('year', 'month').values_list('id', flat=True)
    # Trigger the Celery task with these IDs and the company ID
  # Trigger the task immediately
    task = perform_calculations(financial_asset_ids=list(
        financial_asset_ids), company_id=instance.company.id)
    print(task['data'])
    print(instance.id)
