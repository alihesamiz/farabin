from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import BalanceReport, CompanyProfile, CompanyService, TaxDeclaration, DiagnosticRequest
from .tasks import send_file_uploading_notification


@receiver(post_save, sender=TaxDeclaration)
@receiver(post_save, sender=BalanceReport)
def create_request_if_sent(sender, instance, created, **kwargs):
    if instance.is_sent:
        print(instance)
        try:
            service_instance = CompanyService.objects.get(id=1)
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

# @receiver(post_save, sender=[BalanceReport, TaxDeclaration])
# def send_sms_notification(sender, instance, **kwargs):
#     # Check if `is_sent` is True and `is_saved` is True
#     if instance.is_sent and instance.is_saved:
#         # Call your SMS sending function here
#         message = f"""
#         فایل ترازنامه جدیدی برای شرکت {instance.company.company_title} ارسال شد.
#         """  # Replace with your actual SMS message content.
#         # Use the GeneralUtils class to send the SMS
#         GeneralUtils.send_sms(instance, message)


# @receiver(pre_save, sender=CompanyProfile)
# def handle_company_name_change(sender, instance, **kwargs):
#     # Check if it's an update, not a new creation
#     print(instance.pk)
#     tax_files = (TaxDeclaration.objects.filter(
#         company_id=instance.pk).values_list('tax_file'))
#     print(list(tax_files))
#     if instance.pk and instance.profile_active:
#         try:
#             # Get the previous instance from the database
#             previous_instance = sender.objects.get(pk=instance.pk)
#             previous_slug = GeneralUtils().persian_slugify(previous_instance.company_title)
#             new_slug = GeneralUtils().persian_slugify(instance.company_title)

#             # If the company title has changed, rename the directory
#             if previous_slug != new_slug:
#                 # Define the year and month as per file structure
#                 # year = getattr(instance, 'year', 'unknown-year')

#                 old_tax_folder_path = os.path.join(
#                     settings.MEDIA_ROOT, "financial_files/files/tax_files", previous_slug)
#                 new_tax_folder_path = os.path.join(
#                     settings.MEDIA_ROOT, "financial_files/files/tax_files", new_slug)

#                 old_br_folder_path = os.path.join(
#                     settings.MEDIA_ROOT, "financial_files/files/non-tax_files", previous_slug)
#                 new_br_folder_path = os.path.join(
#                     settings.MEDIA_ROOT, "financial_files/files/non-tax_files", new_slug)

#                 # Check if the old path exists
#                 if os.path.exists(old_tax_folder_path):
#                     # Create the new folder path if it doesn't exist
#                     os.makedirs(new_tax_folder_path, exist_ok=True)

#                     # Move files
#                     for file_name in os.listdir(old_tax_folder_path):
#                         old_file_path = os.path.join(
#                             old_tax_folder_path, file_name)
#                         new_file_path = os.path.join(
#                             new_tax_folder_path, file_name)

#                         # Move (copy and delete) the file to the new path
#                         if old_file_path == new_file_path:
#                             pass
#                             # shutil.move(old_file_path, new_file_path)

#                     # Remove the old directory if it's empty
#                     shutil.rmtree(old_tax_folder_path)

#                 if os.path.exists(old_br_folder_path):
#                     # Create the new folder path if it doesn't exist
#                     os.makedirs(new_br_folder_path, exist_ok=True)

#                     # Move files
#                     for file_name in os.listdir(old_br_folder_path):
#                         old_file_path = os.path.join(
#                             old_br_folder_path, file_name)
#                         new_file_path = os.path.join(
#                             new_br_folder_path, file_name)

#                         # Move (copy and delete) the file to the new path
#                     if old_file_path == new_file_path:
#                         pass
#                         # shutil.move(old_file_path, new_file_path)

#                     # Remove the old directory if it's empty
#                     shutil.rmtree(old_br_folder_path)
#         except sender.DoesNotExist:
#             # The instance is new, so no previous company title exists
#             pass


# @receiver(pre_save, sender=CompanyProfile)
# def handle_company_name_change(sender, instance, **kwargs):
#     # Check if it's an update, not a new creation
#     if instance.pk and instance.profile_active:
#         try:
#             previous_instance = sender.objects.get(pk=instance.pk)
#             previous_slug = GeneralUtils().persian_slugify(previous_instance.company_title)
#             new_slug = GeneralUtils().persian_slugify(instance.company_title)

#             if previous_slug != new_slug:
#                 old_tax_folder_path = os.path.join(
#                     settings.MEDIA_ROOT, "financial_files/files/tax_files", previous_slug)
#                 new_tax_folder_path = os.path.join(
#                     settings.MEDIA_ROOT, "financial_files/files/tax_files", new_slug)

#                 old_br_folder_path = os.path.join(
#                     settings.MEDIA_ROOT, "financial_files/files/non-tax_files", previous_slug)
#                 new_br_folder_path = os.path.join(
#                     settings.MEDIA_ROOT, "financial_files/files/non-tax_files", new_slug)

#                 # Update tax files
#                 if os.path.exists(old_tax_folder_path):
#                     os.makedirs(new_tax_folder_path, exist_ok=True)
#                     for file_name in os.listdir(old_tax_folder_path):
#                         old_file_path = os.path.join(
#                             old_tax_folder_path, file_name)
#                         new_file_path = os.path.join(
#                             new_tax_folder_path, file_name)
#                         shutil.move(old_file_path, new_file_path)
#                         tax_files = TaxDeclaration.objects.filter(
#                             company_id=instance.pk)
#                         if tax_files:
#                             for tax_file in tax_files:
#                                 tax_file.tax_file = f"financial_files/files/tax_files/{
#                                     new_slug}/{file_name}/{file_name}-tax_file.pdf"
#                                 tax_file.save()
#                     shutil.rmtree(old_tax_folder_path)

#                 # Update balance report files similarly
#                 if os.path.exists(old_br_folder_path):
#                     os.makedirs(new_br_folder_path, exist_ok=True)
#                     for file_name in os.listdir(old_br_folder_path):
#                         old_file_path = os.path.join(
#                             old_br_folder_path, file_name)
#                         new_file_path = os.path.join(
#                             new_br_folder_path, file_name)
#                         shutil.move(old_file_path, new_file_path)
#                         print(file_name)

#                         br_files = BalanceReport.objects.filter(
#                             company_id=instance.pk)
#                         if br_files:
#                             for br_file in br_files:
#                                 br_file.balance_report_file = f"financial_files/files/non-tax_files/{
#                                     new_slug}/{file_name}/{file_name}-balance_report_file.pdf"

#                                 br_file.profit_loss_file = f"financial_files/files/non-tax_files/{
#                                     new_slug}/{file_name}/{file_name}-profit_loss_file.pdf"

#                                 br_file.sold_product_file = f"financial_files/files/non-tax_files/{
#                                     new_slug}/{file_name}/{file_name}-sold_product_file.pdf"

#                                 br_file.account_turnover_file = f"financial_files/files/non-tax_files/{
#                                     new_slug}/{file_name}/{file_name}-account_turnover_file.pdf"

#                                 br_file.save()
#                     shutil.rmtree(old_br_folder_path)

#             tax_files = (TaxDeclaration.objects.filter(
#                 company_id=instance.pk).values_list('tax_file'))
#             print(list(tax_files))

#         except sender.DoesNotExist:
#             pass
