from django.db import models
from apps.company.models import CompanyProfile
from constants.validators import Validator as _validator
from apps.core.utils import GeneralUtils
import os

# CurrentAsset – دارایی‌های جاری
# FixedAsset – دارایی های غیر جاری
# CurrentLiability – بدهی‌های جاری
# LongTermLiability – بدهی‌های بلندمدت
# Equity – حقوق صاحبان سهام
# Revenue – درآمدها
# Expense – هزینه ها
# ContingentAccount – حساب‌های انتظامی



def get_bs_file_upload_path(instance, filename):
    path = GeneralUtils(path="bs_files", fields=[""]).rename_folder(instance, filename)
    return path


class BalanceSheet(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, db_index=True)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


    excel_file = models.FileField(
        verbose_name=("فایل اکسل"),
        blank=True,
        null=True,
        upload_to=get_bs_file_upload_path,
        validators=[_validator.excel_file_validator],
    )


    class Meta:
        unique_together = ('company', 'year')  # optional, ensures only one sheet per year
        ordering = ['company', '-year'] 

        verbose_name = "ترازنامه"
        verbose_name_plural = "ترازنامه ها"
  


    def __str__(self):
        return f"Balance Sheet - {self.company.title} - {self.year}"

    def get_all_data(self):

        data = {}
        # Loop through all related objects
        for related_object in self._meta.related_objects:
            related_name = related_object.get_accessor_name()
            related_manager = getattr(self, related_name, None)
            if related_manager is None:
                continue

            items = []
            for obj in related_manager.all():
                obj_data = {}
                for field in obj._meta.fields:
                    if field.name == "id":
                        continue
                    value = getattr(obj, field.name)
                    # Handle JSONField with {"amount": ...}
                    if isinstance(value, dict) and "amount" in value:
                        value = value["amount"]
                    obj_data[field.name] = value  # Use English field names
                items.append(obj_data)

            # Use model class name as key
            model_name = related_object.related_model.__name__
            data[model_name] = items

        return data




    # delete old file when updating with a new file

    def save(self, *args, **kwargs):
        try:
            old_instance = BalanceSheet.objects.get(pk=self.pk)
        except BalanceSheet.DoesNotExist:
            old_instance = None

        super().save(*args, **kwargs)

        # Delete old file if updated
        if old_instance and old_instance.excel_file != self.excel_file:
            if old_instance.excel_file and os.path.exists(old_instance.excel_file.path):
                os.remove(old_instance.excel_file.path)
             






# # Parent
# class BalanceSheet(models.Model):
#     date = models.DateField()

#     # Assets
#     current_assets = models.OneToOneField('CurrentAsset', on_delete=models.CASCADE, null=True, blank=True)
#     non_current_assets = models.OneToOneField('NonCurrentAsset', on_delete=models.CASCADE, null=True, blank=True)

#     # Liabilities
#     current_liabilities = models.OneToOneField('CurrentLiability', on_delete=models.CASCADE, null=True, blank=True)
#     long_term_liabilities = models.OneToOneField('LongTermLiability', on_delete=models.CASCADE, null=True, blank=True)

#     # Equity
#     equity = models.OneToOneField('Equity', on_delete=models.CASCADE, null=True, blank=True)

#     # Income & Expenses
#     revenue = models.OneToOneField('Revenue', on_delete=models.CASCADE, null=True, blank=True)
#     expense = models.OneToOneField('Expense', on_delete=models.CASCADE, null=True, blank=True)

#     # Contingent Accounts
#     contingent_account = models.OneToOneField('ContingentAccount', on_delete=models.CASCADE, null=True, blank=True)

#     def __str__(self):
#         return f"Balance Sheet - {self.date}"

