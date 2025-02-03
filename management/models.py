from django.db import models
from django.utils.translation import gettext_lazy as _


from core import utils
# Create your models here.


def get_hr_file_upload_path(instance, filename):
    path = utils.GeneralUtils(
        path="hr_files", fields=['']).rename_folder(instance, filename)
    return path


class HumanResource(models.Model):
    excel_file = models.FileField(verbose_name=_(
        "Excel File"), blank=False, null=False, upload_to=get_hr_file_upload_path())

    company = models.ForeignKey('company.CompanyProfile', verbose_name=_(
        "Company"), null=False, blank=False)

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Human Resource")
        verbose_name_plural = _("Human Resources")


class PersonelInformation(models.Model):

    name = models.CharField(verbose_name=_("Full Name"),
                            max_length=250, null=False, blank=False)

    unit = models.CharField(verbose_name=_(
        "Unit"), max_length=150, null=False, blank=False)

    position = models.CharField(verbose_name=_(
        "Position"), max_length=150, null=False, blank=False)

    reports_to = models.CharField(verbose_name=_(
        "Reports to(Position)"), max_length=150, null=True, blank=True)

    class Meta:
        verbose_name = _("Personel Information")
        verbose_name_plural = _("Personels Information")
