from django.core.exceptions import ValidationError
from django.db import models
from django.db.transaction import atomic
from django.utils.translation import gettext_lazy as _
from django_lifecycle.conditions import WhenFieldValueChangesTo
from django_lifecycle.decorators import hook
from django_lifecycle.hooks import (
    AFTER_CREATE,
    AFTER_UPDATE,
    BEFORE_CREATE,
    BEFORE_UPDATE,
)
from django_lifecycle.models import LifecycleModelMixin

from apps.core.models import TimeStampedModel


class ExternalFactors(models.TextChoices):
    """External factors"""

    POLITICAL = "Political", _("Political (e.g., regulations, government policies)")
    ECONOMIC = "Economic", _("Economic (e.g., market trends, inflation)")
    SOCIAL = "Social", _("Social (e.g., cultural shifts, demographics)")
    TECHNOLOGICAL = "Technological", _("Technological (e.g., innovation, automation)")
    ENVIRONMENTAL = (
        "Environmental",
        _("Environmental (e.g., sustainability, climate change)"),
    )
    LEGAL = "Legal", _("Legal (e.g., compliance, laws)")
    NONE = "None", _("None")


class SWOTCategory(models.TextChoices):
    STRENGTH = "Strength", _("Strength")
    WEAKNESS = "Weakness", _("Weakness")
    OPPORTUNITY = "Opportunity", _("Opportunity")
    THREAT = "Threat", _("Threat")


class SWOTQuestion(models.Model):
    text = models.TextField(verbose_name=_("Text"), unique=True)
    category = models.CharField(
        max_length=50,
        choices=SWOTCategory.choices,
        verbose_name=_("Category"),
    )

    class Meta:
        verbose_name = _("SWOT Question")
        verbose_name_plural = _("SWOT Questions")

    def __str__(self):
        return f"{self.get_category_display()}: {self.text}"


class SWOTOption(models.Model):
    option = models.CharField(verbose_name=_("Option"), max_length=50)
    category = models.CharField(
        max_length=50,
        choices=SWOTCategory.choices,
        verbose_name=_("Category"),
    )

    def __str__(self):
        return f"{self.option}({self.category})"

    class Meta:
        verbose_name = _("SWOT Option")
        verbose_name_plural = _("SWOT Options")
        constraints = [
            models.UniqueConstraint(
                name="unique_swot_option",
                fields=[
                    "option",
                    "category",
                ],
            )
        ]


class CompanySWOTOption(LifecycleModelMixin, TimeStampedModel):
    company = models.ForeignKey(
        "company.CompanyProfile",
        verbose_name=_("Company"),
        on_delete=models.CASCADE,
    )
    options = models.ManyToManyField(SWOTOption, verbose_name=_("Options"))

    def __str__(self):
        return self.company.title

    class Meta:
        verbose_name = _("Company SWOT Option")
        verbose_name_plural = _("Company SWOT Options")


class CompanySWOTQuestion(LifecycleModelMixin, TimeStampedModel):
    company = models.ForeignKey(
        "company.CompanyProfile",
        verbose_name=_("Company"),
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        SWOTQuestion,
        verbose_name=_("Questions"),
        on_delete=models.PROTECT,
    )
    answer = models.TextField(verbose_name=_("Answer"))
    category = models.CharField(
        max_length=20, choices=SWOTCategory.choices, verbose_name=_("Category")
    )
    external_factor = models.CharField(
        max_length=50,
        choices=ExternalFactors.choices,
        verbose_name=_("External Factor"),
        blank=True,
    )

    def __str__(self):
        if self.question and self.answer:
            return f"{self.get_category_display()}: {self.question.text}"
        return f"{self.get_category_display()}"

    class Meta:
        verbose_name = _("Company SWOT Question")
        verbose_name_plural = _("Company SWOT Questions")
        constraints = [
            models.UniqueConstraint(
                fields=["company", "question"],
                condition=models.Q(question__isnull=False),
                name="unique_company_question",
            )
        ]
        indexes = [
            models.Index(fields=["company", "category"]),
            models.Index(fields=["question"]),
        ]

    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE)
    def set_category_and_validate_external_factors(self):
        self.__set_category()
        self.__check_for_external_factors()
        # self.save()

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
        if self.category in ["opportunity", "threat"] and not self.external_factor:
            self.external_factor = ExternalFactors.NONE
            raise ValidationError(
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
            matrix, created = CompanySWOTQuestionMatrix.objects.get_or_create(
                company=self.company
            )

            # Only add the new option if it's not already there
            if not matrix.questions.filter(id=self.id).exists():
                matrix.questions.add(self)


class BaseSWOTMatrix(LifecycleModelMixin, TimeStampedModel):
    company = models.ForeignKey(
        "company.CompanyProfile",
        verbose_name=_("Company"),
        on_delete=models.CASCADE,
    )
    is_approved = models.BooleanField(_("Is approved"), default=False)

    def __str__(self):
        return f"{self.company.title!r} SWOT"

    def _filter_by_category(self, category):
        return (
            self.get_related_items().select_related("company").filter(category=category)
        )

    @property
    def strengths(self):
        return self._filter_by_category(SWOTCategory.STRENGTH)

    @property
    def weaknesses(self):
        return self._filter_by_category(SWOTCategory.WEAKNESS)

    @property
    def opportunities(self):
        return self._filter_by_category(SWOTCategory.OPPORTUNITY)

    @property
    def threats(self):
        return self._filter_by_category(SWOTCategory.THREAT)

    def get_related_items(self):
        """
        Override this in subclasses to return the related manager (questions/options)
        """
        raise NotImplementedError("Subclasses must implement get_related_items()")

    task_type = None

    @hook(AFTER_UPDATE, condition=WhenFieldValueChangesTo("is_approved", True))
    def start_analysing_task(self):
        from apps.swot.tasks import generate_swot_analysis

        if not self.task_type:
            raise ValueError("Subclasses must define task_type")
        generate_swot_analysis.delay(self.task_type, self.id)

    class Meta:
        abstract = True


class CompanySWOTOptionMatrix(BaseSWOTMatrix):
    options = models.ManyToManyField(
        CompanySWOTOption,
        verbose_name=_("SWOT options"),
        related_name="swot_option_matrices",
    )

    def get_related_items(self):
        return self.options

    task_type = "option"

    class Meta:
        verbose_name = _("Company SWOT(option) Matrix")
        verbose_name_plural = _("Company SWOT(option) Matrices")


class CompanySWOTQuestionMatrix(BaseSWOTMatrix):
    questions = models.ManyToManyField(
        CompanySWOTQuestion,
        verbose_name=_("SWOT questions"),
        related_name="swot_question_matrices",
    )

    def get_related_items(self):
        return self.questions

    task_type = "question"

    class Meta:
        verbose_name = _("Company SWOT(question) Matrix")
        verbose_name_plural = _("Company SWOT(question) Matrices")


class BaseSWOTAnalysis(LifecycleModelMixin, TimeStampedModel):
    so = models.TextField(verbose_name=_("SO Analysis"))
    st = models.TextField(verbose_name=_("ST Analysis"))
    wo = models.TextField(verbose_name=_("WO Analysis"))
    wt = models.TextField(verbose_name=_("WT Analysis"))

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.matrix.company.title}"


class CompanySWOTQuestionAnalysis(BaseSWOTAnalysis):
    matrix = models.ForeignKey(
        CompanySWOTQuestionMatrix,
        verbose_name=_("Matrix"),
        on_delete=models.CASCADE,
        related_name="analysis",
    )

    class Meta:
        verbose_name = _("SWOT Question Analysis")
        verbose_name_plural = _("SWOT Questions Analysis")


class CompanySWOTOptionAnalysis(BaseSWOTAnalysis):
    matrix = models.ForeignKey(
        CompanySWOTOptionMatrix,
        verbose_name=_("Matrix"),
        on_delete=models.CASCADE,
        related_name="analysis",
    )

    class Meta:
        verbose_name = _("SWOT Option Analysis")
        verbose_name_plural = _("SWOT Options Analysis")
