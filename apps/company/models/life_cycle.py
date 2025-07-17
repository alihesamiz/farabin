from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.company.models import CompanyProfile, TimeStampedModel


class LifeCycle(models.Model):
    class LifeCycleChoices(models.TextChoices):
        OPERATIONAL = "operational", _("Operational")
        FINANCE = "finance", _("Finance")
        INVEST = "invest", _("Invest")

    name = models.CharField(
        max_length=11,
        choices=LifeCycleChoices.choices,
        default=LifeCycleChoices.OPERATIONAL,
        verbose_name=_("Name"),
        unique=True,
    )

    class Meta:
        verbose_name = _("Life Cycle")
        verbose_name_plural = _("Life Cycles")

    def __str__(self):
        return self.get_name_display()


class LifeCycleKind(models.TextChoices):
    """Life cycle kind choices."""

    THEORETICAL = "theoretical", _("Theoretical")


class LifeCycleFeature(models.Model):
    """Represents a feature in the life cycle model."""

    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
    )
    weight = models.DecimalField(
        verbose_name=_("Weight"),
        max_digits=5,
        decimal_places=2,
    )

    def __str__(self):
        return f"{self.name}:{self.weight}"

    class Meta:
        verbose_name = _("Life Cycle Feature")
        verbose_name_plural = _("Life Cycle Features")


class LifeCycleDecline(models.Model):
    """Represents a  in the life cycle model."""

    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Life Cycle Decline")
        verbose_name_plural = _("Life Cycle Declines")


class LifeCycleMaturity(models.Model):
    """Represents a  in the life cycle model."""

    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Life Cycle Maturity")
        verbose_name_plural = _("Life Cycle Maturity")


class LifeCycleGrowth(models.Model):
    """Represents a  in the life cycle model."""

    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Life Cycle Growth")
        verbose_name_plural = _("Life Cycle Growth")


class LifeCycleIntroduction(models.Model):
    """Represents a  in the life cycle model."""

    name = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Life Cycle Introduction")
        verbose_name_plural = _("Life Cycle Introduction")


class LifeCycleTheoretical(TimeStampedModel):
    company = models.ForeignKey(
        CompanyProfile,
        verbose_name=_("Company"),
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    feature = models.ForeignKey(
        LifeCycleFeature,
        verbose_name=_("Feature"),
        related_name="life_cycle",
        on_delete=models.CASCADE,
    )
    decline = models.ForeignKey(
        LifeCycleDecline,
        verbose_name=_("Decline"),
        on_delete=models.CASCADE,
        related_name="life_cycle",
    )
    maturity = models.ForeignKey(
        LifeCycleMaturity,
        verbose_name=_("Maturity"),
        on_delete=models.CASCADE,
        related_name="life_cycle",
    )
    growth = models.ForeignKey(
        LifeCycleGrowth,
        verbose_name=_("Growth"),
        on_delete=models.CASCADE,
        related_name="life_cycle",
    )
    introduction = models.ForeignKey(
        LifeCycleIntroduction,
        verbose_name=_("Introduction"),
        on_delete=models.CASCADE,
        related_name="life_cycle",
    )

    class Meta:
        verbose_name = _("Theoretical Life Cycle Place")
        verbose_name_plural = _("Theoretical Life Cycle Place")
        constraints = [
            models.UniqueConstraint(
                name="unique_company_theoretical_place",
                fields=[
                    "company",
                    "feature",
                ],
            )
        ]

    def __str__(self):
        return f"{self.company.title}"

    def _get_weights(self):
        return self.feature.weight


class LifeCycleFinancialResource(models.Model):
    RESOURCE_TYPES = [
        ("operational", _("Operational")),
        ("finance", _("Finance")),
        ("invest", _("Investment")),
    ]

    name = models.CharField(
        max_length=50,
        choices=RESOURCE_TYPES,
        unique=True,
        verbose_name=_("Name"),
    )

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = _("Life Cycle Financial Resource")
        verbose_name_plural = _("Life Cycle Financial Resources")


class LifeCycleQuantitative(TimeStampedModel):
    PLACES = {
        "introduction": ("finance"),
        "growth": ("operational", "finance"),
        "maturity": ("operational"),
        "recession 1": "",
        "recession 2": ("operational", "finance", "invest"),
        "recession 3": ("operational", "invest"),
        "decline 1": ("finance", "invest"),
        "decline 2": ("invest"),
    }

    company = models.ForeignKey(
        CompanyProfile,
        verbose_name=_("Company"),
        on_delete=models.CASCADE,
    )

    resource = models.ManyToManyField(
        LifeCycleFinancialResource,
        verbose_name=_("Resources"),
        related_name="life_cycle",
        blank=True,
    )

    @property
    def place(self):
        resources = set([resource.name for resource in self.resource.all()])
        resources = [resource.name for resource in self.resource.all().order_by("id")]

        for place, values in self.PLACES.items():
            if len(resources) > 1 or len(resources) == 0:
                if list(values) == resources:
                    return place
            else:
                if values == resources[0]:
                    return place
        return None

    def __str__(self):
        resource_names = ", ".join([str(res) for res in self.resource.all()])
        return f"{resource_names!s} - {self.company.company_title!s}"

    class Meta:
        verbose_name = _("Life Cycle Quantitative Position")
        verbose_name_plural = _("Life Cycle Quantitative Positions")
        constraints = [
            models.UniqueConstraint(
                name="unique_company_qunatitative_place", fields=["company"]
            )
        ]
