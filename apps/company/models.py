from uuid import uuid4
import logging

from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError  # noqa: F401
from django.contrib.auth import get_user_model
from django.db import models


from django_lifecycle.mixins import LifecycleModelMixin
from django_lifecycle.hooks import AFTER_CREATE
from django_lifecycle.decorators import hook

from apps.core.validators import Validator as _validator
logger = logging.getLogger("company")

User = get_user_model()


class LifeCycle(models.Model):
    OPERATIONAL = "operational"
    FINANCE = "finance"
    INVEST = "invest"

    LIFE_CYCLE_CHOICES = [
        (OPERATIONAL, _("Operational")),
        (FINANCE, _("Finance")),
        (INVEST, _("Invest")),
    ]
    capital_providing = models.CharField(
        max_length=11,
        choices=LIFE_CYCLE_CHOICES,
        default=OPERATIONAL,
        verbose_name=_("Capital Providing"),
    )

    class Meta:
        verbose_name = _("Life Cycle")
        verbose_name_plural = _("Life Cycles")

    def __str__(self):
        return self.get_capital_providing_display()


class SpecialTech(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = _("Special Tech")
        verbose_name_plural = _("Special Techs")


class TechField(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name = _("Tech Field")
        verbose_name_plural = _("Tech Fields")


class CompanyProfile(LifecycleModelMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="company", verbose_name=_("User")
    )

    company_title = models.CharField(
        max_length=255, verbose_name=_("Company Title"))

    email = models.EmailField(
        max_length=255, unique=True, verbose_name=_("Email"), null=True, blank=True
    )

    manager_social_code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name=_("Manager Social Code"),
        blank=True,
        null=True,
    )

    manager_name = models.CharField(
        max_length=255, verbose_name=_("Manager Full Name"))

    manager_phone_number = models.CharField(
        max_length=11,
        unique=True,
        validators=[_validator.phone_number_model_regex_validator],
        verbose_name=_("Manager Phone Number"),
        null=True,
        blank=True,
    )

    office_phone_number = models.CharField(
        max_length=11,
        unique=True,
        validators=[_validator.landline_number_model_regex_validator],
        verbose_name=_("Office Phone Number"),
        null=True,
        blank=True,
    )

    license = models.ManyToManyField(
        "License", verbose_name=_("License Types"))

    tech_field = models.ForeignKey(
        "TechField",
        default=1,
        on_delete=models.CASCADE,
        verbose_name=_("Technical Field"),
    )

    special_field = models.ForeignKey(
        "SpecialTech",
        default=1,
        on_delete=models.CASCADE,
        verbose_name=_("Special Field"),
    )

    insurance_list = models.PositiveSmallIntegerField(
        default=1, verbose_name=_("Insurance List")
    )

    capital_providing_method = models.ManyToManyField(
        LifeCycle,
        verbose_name=_("Capital Providing Method"),
        related_name="company_profile",
    )

    province = models.ForeignKey(
        "core.Province", default=1, on_delete=models.CASCADE, verbose_name=_("Province")
    )

    city = models.ForeignKey(
        "core.City", default=1, on_delete=models.CASCADE, verbose_name=_("City")
    )

    address = models.CharField(max_length=255, verbose_name=_("Address"))

    is_active = models.BooleanField(
        default=False, verbose_name=_("Is Active?"))

    class Meta:
        verbose_name = _("Company Profile")
        verbose_name_plural = _("Company Profiles")

    def __str__(self) -> str:
        return f"{self.company_title!r} › {self.user.national_code}"

    @hook(AFTER_CREATE)
    def clear_profile_cache(self):
        from django.core.cache import cache

        """
        Hook to clear the cache when a CompanyProfile instance is updated.
        """
        cache_key = f"company_profile_{self.user.id}"
        cache.delete(cache_key)
        logger.info(f"Cleared company profile cache for user {self.user.id}.")


class License(models.Model):
    INDUSTRIAL_TOWN_LICENSE = "itl"
    TECHNOLOGICAL_LICENSE = "tl"
    KNOWLEDGE_BASE_LICENSE = "kbl"
    OTHER_LICENSE = "ol"

    LICENSE_CHOICES = [
        (INDUSTRIAL_TOWN_LICENSE, _("Industrial town")),
        (TECHNOLOGICAL_LICENSE, _("Technological")),
        (KNOWLEDGE_BASE_LICENSE, _("Knowledge base")),
        (OTHER_LICENSE, _("Others")),
    ]

    code = models.CharField(
        max_length=3,
        unique=True,
        choices=LICENSE_CHOICES,
        verbose_name=_("License Code"),
    )
    name = models.CharField(max_length=50, verbose_name=_("License Name"))

    class Meta:
        verbose_name = _("License")
        verbose_name_plural = _("Licenses")

    def __str__(self):
        return self.name


class CompanyService(models.Model):
    company = models.ForeignKey(
        CompanyProfile,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name=_("Company"),
    )
    service = models.ForeignKey(
        "core.Service",
        on_delete=models.CASCADE,
        verbose_name=_("Service"),
        related_name="services",
    )
    is_active = models.BooleanField(default=False, verbose_name=_("Activate"))

    purchased_date = models.DateField(
        auto_now_add=True, verbose_name=_("Purchased Date")
    )

    class Meta:
        unique_together = ("company", "service")
        verbose_name = _("Company Service")
        verbose_name_plural = _("Company Services")

    def __str__(self) -> str:
        return f"{self.company.company_title} › {self.service.name} ({'Active' if self.is_active else 'Inactive'})"


class LifeCycleKind(models.TextChoices):
    """Life cycle kind choices."""

    THEORICAL = "theorical", _("نظری")


class LifeCycleFeature(models.Model):
    """Represents a feature in the life cycle model."""

    name = models.CharField(max_length=255, verbose_name=_("ویژگی"))

    weight = models.DecimalField(verbose_name=_(
        "وزن"), max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = _("چرخه عمر ویژگی‌")
        verbose_name_plural = _("چرخه عمر ویژگی‌ها")

    def __str__(self):
        return f"{self.name}:{self.weight}"


class LifeCycleDecline(models.Model):
    """Represents a  in the life cycle model."""

    name = models.CharField(max_length=255, verbose_name=_("ویژگی"))

    class Meta:
        verbose_name = _("چرخه عمر افول")
        verbose_name_plural = _("چرخه عمر افول")

    def __str__(self):
        return self.name


class LifeCycleMaturity(models.Model):
    """Represents a  in the life cycle model."""

    name = models.CharField(max_length=255, verbose_name=_("ویژگی"))

    class Meta:
        verbose_name = _("چرخه عمر بلوغ")
        verbose_name_plural = _("چرخه عمر بلوغ")

    def __str__(self):
        return self.name


class LifeCycleGrowth(models.Model):
    """Represents a  in the life cycle model."""

    name = models.CharField(max_length=255, verbose_name=_("ویژگی"))

    class Meta:
        verbose_name = _("چرخه عمر رشد")
        verbose_name_plural = _("چرخه عمر رشد")

    def __str__(self):
        return self.name


class LifeCycleIntroduction(models.Model):
    """Represents a  in the life cycle model."""

    name = models.CharField(max_length=255, verbose_name=_("ویژگی"))

    class Meta:
        verbose_name = _("چرخه عمر معرفی")
        verbose_name_plural = _("چرخه عمر معرفی")

    def __str__(self):
        return self.name


class LifeCycleTheoretical(LifecycleModelMixin, models.Model):
    company = models.ForeignKey(
        CompanyProfile,
        verbose_name=_("شرکت"),
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    feature = models.ForeignKey(
        LifeCycleFeature,
        verbose_name=_("ویژگی"),
        related_name="life_cycle",
        on_delete=models.CASCADE,
    )
    decline = models.ForeignKey(
        LifeCycleDecline,
        verbose_name=_("افول"),
        on_delete=models.CASCADE,
        related_name="life_cycle",
    )
    maturity = models.ForeignKey(
        LifeCycleMaturity,
        verbose_name=_("بلوغ"),
        on_delete=models.CASCADE,
        related_name="life_cycle",
    )
    growth = models.ForeignKey(
        LifeCycleGrowth,
        verbose_name=_("رشد"),
        on_delete=models.CASCADE,
        related_name="life_cycle",
    )
    introduction = models.ForeignKey(
        LifeCycleIntroduction,
        verbose_name=_("معرفی"),
        on_delete=models.CASCADE,
        related_name="life_cycle",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("تاریخ ایجاد"))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("تاریخ بروزرسانی"))

    class Meta:
        verbose_name = _("چرخه عمر جایگاه نظری")
        verbose_name_plural = _("چرخه عمر جایگاه نظری")
        constraints = [
            models.UniqueConstraint(
                name="unique_company_theoretical_place", fields=["company", "feature"]
            )
        ]

    def __str__(self):
        return f"{self.get_kind_display()} - {self.company.company_title}"

    def _get_weights(self):
        return self.feature.weight


class LifeCycleFinancialResource(models.Model):
    RESOURCE_TYPES = [
        ("operational", _("عملیاتی")),
        ("finance", _("تامین مالی")),
        ("invest", _("سرمایه گذاری")),
    ]

    name = models.CharField(max_length=50, choices=RESOURCE_TYPES, unique=True)

    class Meta:
        verbose_name = _("چرخه عمر منابع مالی")
        verbose_name_plural = _("چرخه عمر منابع مالی")

    def __str__(self):
        return self.get_name_display()


class LifeCycleQuantitative(models.Model):
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
        verbose_name=_("شرکت"),
        on_delete=models.CASCADE,
    )

    resource = models.ManyToManyField(
        LifeCycleFinancialResource,
        verbose_name=_("منابع"),
        related_name="life_cycle",
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("تاریخ ایجاد"))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("تاریخ بروزرسانی"))

    class Meta:
        verbose_name = _("چرخه عمر جایگاه کمی")
        verbose_name_plural = _("چرخه عمر جایگاه کمی")
        constraints = [
            models.UniqueConstraint(
                name="unique_company_qunatitative_place", fields=["company"]
            )
        ]

    def __str__(self):
        resource_names = ", ".join([str(res) for res in self.resource.all()])
        return f"{resource_names!s} - {self.company.company_title!s}"

    @property
    def place(self):
        resources = set([resource.name for resource in self.resource.all()])
        resources = [
            resource.name for resource in self.resource.all().order_by("id")]

        for place, values in self.PLACES.items():
            if len(resources) > 1 or len(resources) == 0:
                if list(values) == resources:
                    return place
            else:
                if values == resources[0]:
                    return place
        return None


class CompanyQuestionnaire(models.Model):
    company = models.ForeignKey(
        "company.CompanyProfile", on_delete=models.CASCADE, verbose_name=_("شرکت"))
    questionnaire = models.ForeignKey(
        "core.Questionnaire", on_delete=models.CASCADE, verbose_name=_("پرسشنامه"))
    submitted_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("تاریخ ثبت"))

    class Meta:
        verbose_name = _("پرسشنامه شرکت")
        verbose_name_plural = _("پرسشنامه‌های شرکت‌ها")

    def __str__(self):
        return f"{self.company!s} - {self.questionnaire!s}"


class CompanyAnswer(models.Model):
    company_questionnaire = models.ForeignKey(
        "CompanyQuestionnaire", on_delete=models.CASCADE, related_name="answers", verbose_name=_("پرسشنامه‌ شرکت")
    )
    question = models.ForeignKey(
        "core.Question", on_delete=models.CASCADE, verbose_name=_("سوال"))
    selected_choice = models.ForeignKey(
        "core.QuestionChoice", on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("گزینه انتخابی"))
    answered_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("تاریخ پاسخ"))

    class Meta:
        verbose_name = _("پاسخ شرکت")
        verbose_name_plural = _("پاسخ‌های شرکت‌ها")

    def __str__(self):
        return f"{self.question!s}: {self.selected_choice!s}"
