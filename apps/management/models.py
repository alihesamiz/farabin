import logging
import os

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle.conditions import WhenFieldValueChangesTo
from django_lifecycle.decorators import hook
from django_lifecycle.hooks import (
    AFTER_CREATE,
    AFTER_DELETE,
)
from django_lifecycle.mixins import LifecycleModelMixin

from apps.core.models import TimeStampedModel
from apps.core.utils import GeneralUtils
from constants.validators import Validator as _validator

logger = logging.getLogger("management")


def get_hr_file_upload_path(instance, filename):
    path = GeneralUtils(path="hr_files", fields=[""]).rename_folder(instance, filename)
    return path


class HumanResource(LifecycleModelMixin, TimeStampedModel):
    company = models.ForeignKey(
        "company.CompanyProfile",
        verbose_name=_("شرکت"),
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="hrfiles",
    )

    excel_file = models.FileField(
        verbose_name=_("فایل اکسل"),
        blank=False,
        null=False,
        upload_to=get_hr_file_upload_path,
        validators=[_validator.excel_file_validator],
    )

    is_approved = models.BooleanField(verbose_name=_("تأیید شده"), default=False)

    class Meta:
        verbose_name = _("منابع انسانی شرکت‌ها")
        verbose_name_plural = _("منابع انسانی شرکت‌ها")
        constraints = [
            models.UniqueConstraint(fields=["company"], name="unique_company_hr")
        ]

    def __str__(self):
        return f"{self.company.title}"  # › {self.excel_file}"

    @hook(AFTER_CREATE, condition=WhenFieldValueChangesTo("is_approved", True))
    def start_process_personnel_excel(self):
        """
        Hook to start the celery task of proccessing the human reources file
        """
        from management.tasks import process_personnel_excel

        logger.info(
            f"Starting the process of creating personnel information with the id:{self.pk}"
        )
        process_personnel_excel.delay(self.pk)

        logger.info("Process of creating personnel information started successfully.")
        return

    @hook(AFTER_DELETE)
    def delete_hr_file(self):
        """
        Hook to delete the file after deleting the human resource
        """
        file_path = self.excel_file.path
        if os.path.exists(file_path):
            os.remove(file_path)


class Position(models.Model):
    code = models.PositiveIntegerField(verbose_name=_("کد موقعیت"), unique=True)
    position = models.CharField(verbose_name=_("موقعیت"), max_length=150, unique=True)

    class Meta:
        verbose_name = _("موقعیت شغلی")
        verbose_name_plural = _("موقعیت‌های شغلی")
        constraints = [
            models.UniqueConstraint(
                fields=["code", "position"], name="unique_position_code"
            )
        ]

    def __str__(self):
        return f"{self.code}:{self.position}"


class PersonelInformation(models.Model):
    human_resource = models.ForeignKey(
        HumanResource,
        verbose_name=_("منابع انسانی"),
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="personelinformation",
    )

    name = models.CharField(
        verbose_name=_("نام کامل"), max_length=250, null=False, blank=False
    )

    position = models.CharField(
        verbose_name=_("موقعیت شغلی"), max_length=150, null=False, blank=False
    )

    reports_to = models.ManyToManyField(
        "self", verbose_name=_("گزارش به (پرسنل)"), blank=True
    )

    cooperates_with = models.ManyToManyField(
        "self", verbose_name=_("همکاری با (پرسنل)"), blank=True
    )

    obligations = models.TextField(verbose_name=_("وظایف"), null=False, blank=False)

    is_exist = models.BooleanField(verbose_name=_("موجود است"), default=False)

    class Meta:
        verbose_name = _("اطلاعات پرسنل")
        verbose_name_plural = _("اطلاعات پرسنل")

    def __str__(self):
        return f"{self.name}"


def get_chart_excel_file_upload_path(instance, filename):
    path = GeneralUtils(path="chart_excel_files", fields=["field"]).rename_folder(
        instance, filename
    )
    return path


class OrganizationChartBase(LifecycleModelMixin, models.Model):
    field = models.CharField(
        verbose_name=_("زمینه"), max_length=150, null=False, blank=False
    )

    position_excel = models.FileField(
        verbose_name=_("فایل اکسل موقعیت"),
        max_length=150,
        null=False,
        blank=False,
        upload_to=get_chart_excel_file_upload_path,
        validators=[_validator.excel_file_validator],
    )

    class Meta:
        verbose_name = _("فایل‌ خام نمودار سازمانی")
        verbose_name_plural = _("فایل‌های خام نمودار سازمانی")

    def __str__(self):
        return f"{self.field.title()}"

    @hook(AFTER_DELETE)
    def delete_hr_file(self):
        """
        Hook to delete the file after deleting the record
        """
        file_path = self.position_excel.path
        if os.path.exists(file_path):
            os.remove(file_path)
