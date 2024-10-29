# reporting/signals.py
from .models import BalanceReport ,TaxDeclaration
from django.db.models.signals import post_save
from django.dispatch import receiver
from core.utils import GeneralUtils
@receiver(post_save, sender=[BalanceReport,TaxDeclaration])
def send_sms_notification(sender, instance, **kwargs):
    # Check if `is_sent` is True and `is_saved` is True
    if instance.is_sent and instance.is_saved:
        # Call your SMS sending function here
        message = f"""
        فایل ترازنامه جدیدی برای شرکت {instance.company.company_title} ارسال شد.
        """  # Replace with your actual SMS message content.
        # Use the GeneralUtils class to send the SMS
        GeneralUtils.send_sms(instance,message)