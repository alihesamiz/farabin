from django.db import models
from django.utils.translation import gettext_lazy as _

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


class SWOTModelMatrix(TimeStampedModel):
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
    opportunity = models.JSONField(verbose_name=_("Opportunity"))
    threat = models.JSONField(verbose_name=_("Threat"))
    weakness = models.JSONField(verbose_name=_("Weakness"))
    strength = models.JSONField(verbose_name=_("Strength"))

    def __str__(self):
        return self.company.title

    class Meta:
        verbose_name = _("SWOT Matrix")
        verbose_name_plural = _("SWOT Matrices")
