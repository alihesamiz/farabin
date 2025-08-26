import logging
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel
from apps.core.utils import GeneralUtils
from constants.validators import Validator as _validator

logger = logging.getLogger("company")

User = get_user_model()


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
    name = models.CharField(
        max_length=50,
        verbose_name=_("License Name"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("License")
        verbose_name_plural = _("Licenses")


def set_company_logo_path(instance, filename) -> str:
    return GeneralUtils(path="companies_logo", fields=["title"]).rename_folder(
        instance, filename
    )

 
class CompanyProfile(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )
    title = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        verbose_name=_("Company Title"),
    )
    logo = models.ImageField(
        _("Logo"),
        upload_to=set_company_logo_path,
        validators=[_validator.image_file_validator],
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name=_("Email"),
        null=True,
        blank=True,
    )
    national_code = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        verbose_name=_("Company National Registration Code"),
    )
    office_phone_number = models.CharField(
        max_length=11,
        unique=True,
        validators=[_validator.landline_number_model_regex_validator()],
        verbose_name=_("Office Phone Number"),
        null=True,
        blank=True,
    )
    license = models.ManyToManyField(
        "License",
        verbose_name=_("License Types"),
    )
    tech_field = models.ForeignKey(
        "TechField",
        default=1,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("Technical Field"),
    )
    special_field = models.ForeignKey(
        "SpecialTech",
        default=1,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("Special Field"),
    )
    insurance_list = models.PositiveSmallIntegerField(
        default=1,
        null=True,
        verbose_name=_("Insurance List Count"),
    )
    capital_providing_method = models.ManyToManyField(
        "company.LifeCycle",
        related_name="company_profile",
        verbose_name=_("Capital Providing Method"),
    )
    province = models.ForeignKey(
        "core.Province",
        default=1,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("Province"),
    )
    city = models.ForeignKey(
        "core.City",
        default=1,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_("City"),
    )
    address = models.CharField(
        max_length=255,
        null=True,
        verbose_name=_("Address"),
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name=_("Is Active?"),
    )
    upstream_industries = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Upstream Industries"),
    )
    downstream_industries = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("Downstream Industries"),
    )

    @property
    def is_profile_complete(self):
        for field in self._meta.fields:
            if field.name in [
                "id",
                "created_at",
                "updated_at",
                "deleted_at",
                "logo",
            ]:
                continue
            value = getattr(self, field.name)
            if value in [None, "", []]:
                return False
        return True

    def __str__(self) -> str:
        return f"{self.title!r}"

    class Meta:
        verbose_name = _("Company Profile")
        verbose_name_plural = _("Company Profiles")


class CompanyUser(TimeStampedModel):
    class Role(models.TextChoices):
        MANAGER = "manager", _("Manager")
        ADMIN = "admin", _("Admin")
        STAFF = "staff", _("Staff")

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="company_user",
        verbose_name=_("Company User"),
    )
    company = models.ForeignKey(
        CompanyProfile,
        on_delete=models.CASCADE,
        related_name="company_user",
        verbose_name=_("Company"),
        null=True,
        blank=True,
    )
    role = models.CharField(
        choices=Role.choices,
        default=Role.STAFF,
        max_length=7,
        verbose_name=_("Role"),
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Deleted At"),
    )

    def __str__(self):
        return f"{self.company} {self.user}"

    class Meta:
        verbose_name = _("Company User")
        verbose_name_plural = _("Company Users")
        constraints = [
            models.UniqueConstraint(
                fields=["company", "user"],
                name="unique_user_per_company",
            ),
            models.UniqueConstraint(
                fields=["company"],
                condition=models.Q(role="manager"),
                name="unique_manager_per_company",
            ),
        ]


class CompanyService(models.Model):
    company = models.ForeignKey(
        CompanyProfile,
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name=_("Company"),
    )
    service = models.ForeignKey(
        "packages.Service",
        on_delete=models.CASCADE,
        related_name="services",
        verbose_name=_("Service"),
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name=_("Activate"),
    )
    purchased_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Purchased At"),
    )
    deleted_at = models.DateTimeField(
        verbose_name=_("Deleted At"),
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.company.title} › {self.service.name} ({'Active' if self.is_active else 'Inactive'})"

    class Meta:
        verbose_name = _("Company Service")
        verbose_name_plural = _("Company Services")
        constraints = [
            models.UniqueConstraint(
                name="unique_company_service",
                fields=[
                    "company",
                    "service",
                ],
            )
        ]


class ServiceName(models.TextChoices):
    FINANCIAL = "financial", _("Financial")
    MANAGEMENT = "management", _("Management")
    MIS = "mis", _("MIS")
    RAD = "rad", _("R&D")
    MARKETING = "marketing", _("Marketing")
    PRODUCTION = "production", _("Production")


class CompanyUserServicePermission(TimeStampedModel):
    company_user = models.ForeignKey(
        CompanyUser,
        on_delete=models.CASCADE,
        related_name="service_permissions",
        verbose_name=_("Company User"),
    )
    service = models.CharField(
        max_length=10,
        verbose_name=_("Service"),
        choices=ServiceName.choices,
    )
    deleted_at = models.DateTimeField(
        verbose_name=_("Deleted At"),
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.company_user}: {self.service}"

    class Meta:
        verbose_name = _("Company User Service Permission")
        verbose_name_plural = _("Company User Service Permissions")
        constraints = [
            models.UniqueConstraint(
                name="unique_company_user_service_permission",
                fields=[
                    "company_user",
                    "service",
                ],
            )
        ]
