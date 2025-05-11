from uuid import uuid4
import logging

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db import models


from django_lifecycle.mixins import LifecycleModelMixin
from django_lifecycle.hooks import AFTER_CREATE
from django_lifecycle.decorators import hook

from core.validators import phone_number_validator, landline_number_validator

logger = logging.getLogger("company")

User = get_user_model()


class LifeCycle(models.Model):
    OPERATIONAL = 'operational'
    FINANCE = 'finance'
    INVEST = 'invest'

    LIFE_CYCLE_CHOICES = [
        (OPERATIONAL, _('Operational')),
        (FINANCE, _('Finance')),
        (INVEST, _('Invest')),
    ]
    capital_providing = models.CharField(
        max_length=11, choices=LIFE_CYCLE_CHOICES, default=OPERATIONAL, verbose_name=_("Capital Providing"))

    class Meta:
        verbose_name = _('Life Cycle')
        verbose_name_plural = _('Life Cycles')

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
        User, on_delete=models.CASCADE, related_name='company', verbose_name=_("User"))

    company_title = models.CharField(
        max_length=255, verbose_name=_("Company Title"))

    email = models.EmailField(
        max_length=255, unique=True, verbose_name=_("Email"), null=True, blank=True)

    manager_social_code = models.CharField(
        max_length=10, unique=True, verbose_name=_("Manager Social Code"), blank=True, null=True)

    manager_name = models.CharField(
        max_length=255, verbose_name=_("Manager Full Name"))

    manager_phone_number = models.CharField(
        max_length=11, unique=True, validators=[phone_number_validator], verbose_name=_("Manager Phone Number"), null=True, blank=True)

    office_phone_number = models.CharField(
        max_length=11, unique=True, validators=[landline_number_validator], verbose_name=_("Office Phone Number"), null=True, blank=True)

    license = models.ManyToManyField(
        'License', verbose_name=_("License Types"))

    tech_field = models.ForeignKey('TechField', default=1,
                                   on_delete=models.CASCADE,
                                   verbose_name=_("Technical Field"))

    special_field = models.ForeignKey('SpecialTech', default=1,
                                      on_delete=models.CASCADE,
                                      verbose_name=_("Special Field")
                                      )

    insurance_list = models.PositiveSmallIntegerField(
        default=1, verbose_name=_("Insurance List"))

    capital_providing_method = models.ManyToManyField(
        LifeCycle, verbose_name=_('Capital Providing Method'), related_name='company_profile')

    province = models.ForeignKey(
        'core.Province', default=1, on_delete=models.CASCADE, verbose_name=_("Province"))

    city = models.ForeignKey(
        'core.City', default=1, on_delete=models.CASCADE, verbose_name=_("City"))

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
        logger.info(
            f"Cleared company profile cache for user {self.user.id}.")


class License(models.Model):
    INDUSTRIAL_TOWN_LICENSE = 'itl'
    TECHNOLOGICAL_LICENSE = 'tl'
    KNOWLEDGE_BASE_LICENSE = 'kbl'
    OTHER_LICENSE = 'ol'

    LICENSE_CHOICES = [
        (INDUSTRIAL_TOWN_LICENSE, _("Industrial town")),
        (TECHNOLOGICAL_LICENSE, _("Technological")),
        (KNOWLEDGE_BASE_LICENSE, _("Knowledge base")),
        (OTHER_LICENSE, _("Others")),
    ]

    code = models.CharField(max_length=3, unique=True,
                            choices=LICENSE_CHOICES, verbose_name=_("License Code"))
    name = models.CharField(max_length=50, verbose_name=_("License Name"))

    class Meta:
        verbose_name = _("License")
        verbose_name_plural = _("Licenses")

    def __str__(self):
        return self.name


class CompanyService(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE,
                                related_name='services', verbose_name=_("Company"))
    service = models.ForeignKey(
        'core.Service', on_delete=models.CASCADE, verbose_name=_("Service"), related_name='services')
    is_active = models.BooleanField(default=False, verbose_name=_("Activate"))

    purchased_date = models.DateField(
        auto_now_add=True, verbose_name=_("Purchased Date"))

    class Meta:
        unique_together = ("company", "service")
        verbose_name = _("Company Service")
        verbose_name_plural = _("Company Services")

    def __str__(self) -> str:
        return f"{self.company.company_title} › {self.service.name} ({'Active' if self.is_active else 'Inactive'})"
