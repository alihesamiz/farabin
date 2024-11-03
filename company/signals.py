# reporting/signals.py
from django.conf import settings
import os
import shutil
from django.core.files.storage import default_storage
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import BalanceReport, CompanyProfile, TaxDeclaration
from core.utils import GeneralUtils


@receiver(post_save, sender=[BalanceReport, TaxDeclaration])
def send_sms_notification(sender, instance, **kwargs):
    # Check if `is_sent` is True and `is_saved` is True
    if instance.is_sent and instance.is_saved:
        # Call your SMS sending function here
        message = f"""
        فایل ترازنامه جدیدی برای شرکت {instance.company.company_title} ارسال شد.
        """  # Replace with your actual SMS message content.
        # Use the GeneralUtils class to send the SMS
        GeneralUtils.send_sms(instance, message)


@receiver(pre_save, sender=CompanyProfile)
def handle_company_name_change(sender, instance, **kwargs):
    # Check if it's an update, not a new creation
    if instance.pk and instance.profile_active:
        try:
            # Get the previous instance from the database
            previous_instance = sender.objects.get(pk=instance.pk)
            previous_slug = GeneralUtils().persian_slugify(previous_instance.company_title)
            new_slug = GeneralUtils().persian_slugify(instance.company_title)

            # If the company title has changed, rename the directory
            if previous_slug != new_slug:
                # Define the year and month as per file structure
                # year = getattr(instance, 'year', 'unknown-year')

                old_tax_folder_path = os.path.join(
                    settings.MEDIA_ROOT, "financial_files/files/tax_files", previous_slug)
                new_tax_folder_path = os.path.join(
                    settings.MEDIA_ROOT, "financial_files/files/tax_files", new_slug)

                old_br_folder_path = os.path.join(
                    settings.MEDIA_ROOT, "financial_files/files/non-tax_files", previous_slug)
                new_br_folder_path = os.path.join(
                    settings.MEDIA_ROOT, "financial_files/files/non-tax_files", new_slug)

                # Check if the old path exists
                if os.path.exists(old_tax_folder_path):
                    # Create the new folder path if it doesn't exist
                    os.makedirs(new_tax_folder_path, exist_ok=True)

                    # Move files
                    for file_name in os.listdir(old_tax_folder_path):
                        old_file_path = os.path.join(
                            old_tax_folder_path, file_name)
                        new_file_path = os.path.join(
                            new_tax_folder_path, file_name)

                        # Move (copy and delete) the file to the new path
                        if old_file_path == new_file_path:
                            shutil.move(old_file_path, new_file_path)

                    # Remove the old directory if it's empty
                    shutil.rmtree(old_tax_folder_path)

                if os.path.exists(old_br_folder_path):
                    # Create the new folder path if it doesn't exist
                    os.makedirs(new_br_folder_path, exist_ok=True)

                    # Move files
                    for file_name in os.listdir(old_br_folder_path):
                        old_file_path = os.path.join(
                            old_br_folder_path, file_name)
                        new_file_path = os.path.join(
                            new_br_folder_path, file_name)

                        # Move (copy and delete) the file to the new path
                    if old_file_path == new_file_path:
                        shutil.move(old_file_path, new_file_path)

                    # Remove the old directory if it's empty
                    shutil.rmtree(old_br_folder_path)
        except sender.DoesNotExist:
            # The instance is new, so no previous company title exists
            pass
