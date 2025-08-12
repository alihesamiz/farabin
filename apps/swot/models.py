from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_lifecycle import AFTER_SAVE, LifecycleModelMixin, hook

from apps.core.models import TimeStampedModel
from apps.swot.tasks import generate_swot_analysis


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


class SWOTJSONField(models.JSONField):
    """Json custom field for swot properties

    only the key value pairs with this format are allowed:
    >>> key : "value"

    which the keys are the IDs for the matrix property type and the values are the -
    user values or the pre-existing selective values
    """

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        self._validate_swot_format(value)

    def _validate_swot_format(self, value):
        """Validate that JSON has integer keys and string values"""
        if not isinstance(value, dict):
            raise ValidationError(_("Field must be a dictionary object."))

        for key, val in value.items():
            if isinstance(key, str):
                try:
                    int(key)
                except ValueError:
                    raise ValidationError(
                        _(
                            "Keys must be integers or string representations of integers."
                        )
                    )
            elif not isinstance(key, int):
                raise ValidationError(
                    _("Keys must be integers or string representations of integers.")
                )

            # Check value is string
            if not isinstance(val, str):
                raise ValidationError(_("Values must be strings."))


class SWOTMatrix(LifecycleModelMixin, TimeStampedModel):
    class SWOTMatrixType(models.TextChoices):
        QUESTIONNAIRE = "q", _("Questionnaire")
        INFERENTIAL = "i", _("Inferential")
        ELECTIVE = "e", _("Elective")

    company = models.ForeignKey(
        "company.CompanyProfile",
        verbose_name=_("Company"),
        on_delete=models.CASCADE,
        related_name="swot",
    )
    matrix_type = models.CharField(
        max_length=15, verbose_name=_("Type"), choices=SWOTMatrixType.choices
    )

    opportunity = SWOTJSONField(verbose_name=_("Opportunity"))
    threat = SWOTJSONField(verbose_name=_("Threat"))
    weakness = SWOTJSONField(verbose_name=_("Weakness"))
    strength = SWOTJSONField(verbose_name=_("Strength"))

    def __str__(self):
        return self.company.title

    @hook(AFTER_SAVE)
    def start_analysis_generation(self):
        generate_swot_analysis.delay(self.pk)

    class Meta:
        verbose_name = _("SWOT Matrix")
        verbose_name_plural = _("SWOT Matrices")


class SWOTAnalysis(TimeStampedModel):
    matrix = models.ForeignKey(
        SWOTMatrix,
        verbose_name=_("Matrix"),
        on_delete=models.CASCADE,
        related_name="analysis",
    )

    so = models.TextField(verbose_name=_("SO Analysis"))
    st = models.TextField(verbose_name=_("ST Analysis"))
    wo = models.TextField(verbose_name=_("WO Analysis"))
    wt = models.TextField(verbose_name=_("WT Analysis"))

    def __str__(self):
        return f"{self.matrix.company.title}"

    class Meta:
        verbose_name = _("SWOT Analysis")
        verbose_name_plural = _("SWOT Analysis")
        ordering = ["-created_at"]
