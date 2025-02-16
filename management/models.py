from django.db import models
from django.utils.translation import gettext_lazy as _


from core.validators import excel_file_validator
from core.utils import GeneralUtils


def get_hr_file_upload_path(instance, filename):
    path = GeneralUtils(
        path="hr_files", fields=['']).rename_folder(instance, filename)
    return path


class HumanResource(models.Model):
    excel_file = models.FileField(verbose_name=_(
        "Excel File"), blank=False, null=False, upload_to=get_hr_file_upload_path, validators=[excel_file_validator])

    company = models.ForeignKey('company.CompanyProfile', verbose_name=_(
        "Company"), null=False, blank=False, on_delete=models.CASCADE, related_name="hrfiles")

    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company.company_title}"# › {self.excel_file}"
    
    class Meta:
        verbose_name = _("Human Resource")
        verbose_name_plural = _("Human Resources")
        constraints = [
            models.UniqueConstraint(
                fields=['company'], name='unique_company_hr')
        ]


class PersonelInformation(models.Model):

    human_resource = models.ForeignKey(HumanResource, verbose_name=_(
        "Human Resource"), null=False, blank=False, on_delete=models.CASCADE, related_name='personelinformation')

    name = models.CharField(verbose_name=_("Full Name"),
                            max_length=250, null=False, blank=False)

    unit = models.CharField(verbose_name=_(
        "Unit"), max_length=150, null=False, blank=False)

    position = models.CharField(verbose_name=_(
        "Position"), max_length=150, null=False, blank=False)

    reports_to = models.CharField(verbose_name=_(
        "Reports to(Position)"), max_length=150, null=True, blank=True)
    
    def __str__(self):
        return f"{self.human_resource.company.company_title} › {self.position}"
    class Meta:
        verbose_name = _("Personel Information")
        verbose_name_plural = _("Personels Information")


def get_chart_excel_file_upload_path(instance, filename):
    path = GeneralUtils(
        path="chart_excel_files", fields=['field']).rename_folder(instance, filename)
    return path


class OrganizationChartBase(models.Model):
    
    field = models.CharField(verbose_name=_("Field"), max_length=150, null=False, blank=False)
    
    position_excel = models.FileField(verbose_name=_("Position Excel"), max_length=150, null=False, blank=False,
                                      upload_to=get_chart_excel_file_upload_path, validators=[excel_file_validator])

    def __str__(self):
        return f"{self.field.title()}"
    
    class Meta:
        verbose_name = _("Organization Chart")
        verbose_name_plural = _("Organization Charts")
