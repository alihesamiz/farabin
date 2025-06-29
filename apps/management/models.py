import logging
import os

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.transaction import atomic
from django.db import models

from django_lifecycle.hooks import (
    BEFORE_CREATE,
    BEFORE_UPDATE,
    AFTER_CREATE,
    AFTER_UPDATE,
    AFTER_DELETE,
)
from django_lifecycle.conditions import WhenFieldValueChangesTo
from django_lifecycle.mixins import LifecycleModelMixin
from django_lifecycle.decorators import hook

from apps.core.validators import Validator as _validator
from apps.core.utils import GeneralUtils


logger = logging.getLogger("management")


def get_hr_file_upload_path(instance, filename):
    path = GeneralUtils(path="hr_files", fields=[
                        ""]).rename_folder(instance, filename)
    return path


class HumanResource(LifecycleModelMixin, models.Model):
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

    is_approved = models.BooleanField(
        verbose_name=_("تأیید شده"), default=False)

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("تاریخ ایجاد"))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("تاریخ بروزرسانی"))

    class Meta:
        verbose_name = _("منابع انسانی شرکت‌ها")
        verbose_name_plural = _("منابع انسانی شرکت‌ها")
        constraints = [
            models.UniqueConstraint(
                fields=["company"], name="unique_company_hr")
        ]

    def __str__(self):
        return f"{self.company.company_title}"  # › {self.excel_file}"

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

        logger.info(
            "Process of creating personnel information started successfully.")
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
    code = models.PositiveIntegerField(
        verbose_name=_("کد موقعیت"), unique=True)
    position = models.CharField(verbose_name=_(
        "موقعیت"), max_length=150, unique=True)

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

    @classmethod
    def get_postition_by_code(cls, code: int):
        try:
            return cls.objects.get(code=code).position
        except Exception:
            raise Exception(f"No position found with the given code {code}")


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

    obligations = models.TextField(
        verbose_name=_("وظایف"), null=False, blank=False)

    is_exist = models.BooleanField(verbose_name=_("موجود است"), default=False)

    class Meta:
        verbose_name = _("اطلاعات پرسنل")
        verbose_name_plural = _("اطلاعات پرسنل")

    def __str__(self):
        return f"{self.name}"

    @classmethod
    def grouped_chart_data(cls, company):
        """
        This functions gather the data for each person with the aggregated
        'reports-to' and 'cooperates-with' values
        """
        queryset = cls.objects.prefetch_related("human_resource__company").filter(
            human_resource__company=company
        )
        grouped_data = {}

        for person in queryset:
            pos = person.position
            name = person.name
            key = (pos, name)

            if key not in grouped_data:
                grouped_data[key] = {
                    "personnel": [],
                    "aggregated_reports_to": set(),
                    "aggregated_cooperates_with": set(),
                }
            grouped_data[key]["personnel"].append(person.position)

            if person.reports_to.exists():
                for report in person.reports_to.all():
                    grouped_data[key]["aggregated_reports_to"].add(
                        (report.position, report.name)
                    )

            if person.cooperates_with.exists():
                for cooperate in person.cooperates_with.all():
                    grouped_data[key]["aggregated_cooperates_with"].add(
                        (cooperate.position, cooperate.name)
                    )

        response_data = {}
        for (pos, name), data in grouped_data.items():
            response_data[f"{pos} | {name}"] = {
                "aggregated_reports_to": [
                    {"position": position, "name": report_name}
                    for position, report_name in data["aggregated_reports_to"]
                ],
                "aggregated_cooperates_with": [
                    {"position": position, "name": cooperate_name}
                    for position, cooperate_name in data["aggregated_cooperates_with"]
                ],
            }

        return response_data


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


class ExternalFactors(models.TextChoices):
    """External factors"""

    POLITICAL = "Political", _("سیاسی (مانند مقررات، سیاست‌های دولتی)")
    ECONOMIC = "Economic", _("اقتصادی (مانند روندهای بازار، تورم)")
    SOCIAL = "Social", _("اجتماعی (مانند تغییرات فرهنگی، جمعیت‌شناسی)")
    TECHNOLOGICAL = "Technological", _("فناوری (مانند نوآوری، اتوماسیون)")
    ENVIRONMENTAL = "Environmental", _(
        "محیطی (مانند پایداری، تغییرات آب و هوایی)")
    LEGAL = "Legal", _("قانونی (مانند انطباق، قوانین)")
    NONE = "None", _("هیچ‌کدام")


class SWOTCategory(models.TextChoices):
    STRENGTH = "Strength", _("نقطه قوت")
    WEAKNESS = "Weakness", _("نقطه ضعف")
    OPPORTUNITY = "Opportunity", _("فرصت")
    THREAT = "Threat", _("تهدید")


class SWOTQuestion(models.Model):
    text = models.TextField(verbose_name=_("سوال"), unique=True)
    category = models.CharField(
        max_length=50,
        choices=SWOTCategory.choices,
        verbose_name=_("دسته‌بندی"),
    )

    class Meta:
        verbose_name = _("SWOT سوال")
        verbose_name_plural = _("SWOT سوالات")

    def __str__(self):
        return f"{self.get_category_display()}: {self.text}"


class SWOTOption(LifecycleModelMixin, models.Model):
    company = models.ForeignKey(
        "company.CompanyProfile",
        verbose_name=_("شرکت"),
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    question = models.ForeignKey(
        SWOTQuestion,
        verbose_name=_("سوال"),
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    answer = models.TextField(verbose_name=_("پاسخ"), blank=True, null=True)
    category = models.CharField(
        max_length=20, choices=SWOTCategory.choices, verbose_name=_("دسته‌بندی")
    )
    external_factor = models.CharField(
        max_length=50,
        choices=ExternalFactors.choices,
        verbose_name=_("عامل خارجی"),
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("تاریخ ایجاد"))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("تاریخ بروزرسانی"))

    class Meta:
        verbose_name = _("SWOT گزینه")
        verbose_name_plural = _("SWOT گزینه‌ها")
        constraints = [
            models.UniqueConstraint(
                fields=["company", "question", "category"],
                condition=models.Q(question__isnull=False),
                name="unique_company_question_category",
            )
        ]
        indexes = [
            models.Index(fields=["company", "category"]),
            models.Index(fields=["question"]),
        ]

    def __str__(self):
        if self.question and self.answer:
            return f"{self.get_category_display()}: {self.question.text}"
        return f"{self.get_category_display()}"

    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE)
    def set_category_and_validate_external_factors(self):
        self.__set_category()
        self.__check_for_external_factors()

    def __set_category(self):
        """
        Set the category for each option as the questions category
        """
        if self.question:
            self.category = self.question.category

    def __check_for_external_factors(self):
        """
        If the category is either opportunity or theat asks for the external factor if none is provided
        """
        if self.category in ["Opportunity", "Threat"] and not self.external_factor:
            self.external_factor = ExternalFactors.NONE
            return ValidationError(
                {
                    "external_factor": _(
                        "External factor must be specified for Opportunities and Threats."
                    )
                }
            )

    @hook(AFTER_CREATE)
    @hook(AFTER_UPDATE)
    def create_or_update_swot_matrix_after_new_options_addition(self):
        """
        After each SWOTOption is created or updated, this hook checks if the corresponding
        SWOTMatrix for the company exists. If it does, it adds the new option; if not, it creates it.
        """
        with atomic():
            matrix, created = SWOTMatrix.objects.get_or_create(
                company=self.company)

            # Only add the new option if it's not already there
            if not matrix.options.filter(id=self.id).exists():
                matrix.options.add(self)


class SWOTMatrix(LifecycleModelMixin, models.Model):
    company = models.ForeignKey(
        "company.CompanyProfile",
        verbose_name=_("شرکت"),
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="swot_matrices",
    )
    options = models.ManyToManyField(
        SWOTOption, verbose_name=_("گزینه‌های SWOT"), related_name="swot_matrices"
    )
    is_approved = models.BooleanField(
        _("مورد تایید قرار گرفته است"), default=False)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("تاریخ ایجاد"))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("تاریخ بروزرسانی"))

    class Meta:
        verbose_name = _("SWOT ماتریس")
        verbose_name_plural = _("SWOT ماتریس‌ها")
        constraints = [
            models.UniqueConstraint(
                fields=["company"], name="unique_company_swot")
        ]

    def __str__(self):
        return f"{self.company.company_title!r} SWOT"

    @hook(AFTER_UPDATE, condition=WhenFieldValueChangesTo("is_approved", True))
    def start_analysing_task(self):
        """
        Hook to start the SWOT analyze process when the matrix 'is_approved'
        """
        from management.tasks import generate_swot_analysis

        generate_swot_analysis.delay(self.id)

    @property
    def strengths(self):
        return self.options.filter(category="Strength")

    @property
    def weaknesses(self):
        return self.options.filter(category="Weakness")

    @property
    def opportunities(self):
        return self.options.filter(category="Opportunity")

    @property
    def threats(self):
        return self.options.filter(category="Threat")


class SWOTAnalysis(LifecycleModelMixin, models.Model):
    matrix = models.ForeignKey(
        SWOTMatrix,
        verbose_name=_("ماتریس"),
        on_delete=models.CASCADE,
        related_name="analysis",
    )

    so = models.TextField(verbose_name=_("تحلیل نقاط قوت و فرصت‌ها"))
    st = models.TextField(verbose_name=_("تحلیل نقاط قوت و تهدیدات"))
    wo = models.TextField(verbose_name=_("تحلیل نقاط ضعف و فرصت‌ها"))
    wt = models.TextField(verbose_name=_("تحلیل نقاط ضعف و تهدیدات"))

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("تاریخ ایجاد"))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("تاریخ بروزرسانی"))

    class Meta:
        verbose_name = _("SWOT تحلیل")
        verbose_name_plural = _("SWOT تحلیل‌ها")
        constraints = [
            models.UniqueConstraint(
                fields=["matrix"], name="unique_matrix_analysis_swot"
            )
        ]

    def __str__(self):
        return f"{self.matrix.company.company_title}"
