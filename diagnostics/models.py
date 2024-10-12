import random
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import AbstractBaseUser as BaseUser


from .managers import UserManager
# Create your models here.


class User(BaseUser):

    phone_number = models.CharField(max_length=13, unique=True)
    national_code = models.CharField(max_length=20, unique=True)
    otp = models.CharField(max_length=6)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'national_code'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.phone_number}"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    @property
    def is_admin(self):
        return self.is_superuser


class OTP(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='+')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # OTP is valid for 10 minutes
        return self.created_at >= timezone.now() - timedelta(minutes=10)

    def generate_otp(self):
        return random.randint(100000, 999999)


class CompanyProfile(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid4)

    NEWBIE_LICENSE = 'newbie'
    INNOVATIVE_LICENSE = 'innovative'
    TECHNOLOGICAL_LICENSE = 'technological'
    LICENSE_CHOICES = [
        (NEWBIE_LICENSE, _("Newbie")),
        (INNOVATIVE_LICENSE, _("Innovative")),
        (TECHNOLOGICAL_LICENSE, _("Technological")),
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_("User"))

    company_title = models.CharField(
        max_length=255, verbose_name=_("Company Title"))

    email = models.EmailField(
        max_length=255, unique=True, verbose_name=_("EMail"))

    social_code = models.CharField(
        max_length=10, unique=True, verbose_name=_("Social Code"))

    manager_name = models.CharField(
        max_length=255, verbose_name=_("Manager Full Name"))

    license = models.CharField(
        max_length=15, choices=LICENSE_CHOICES, verbose_name=_("License Type"))

    work_place = models.ForeignKey(
        'Institute', on_delete=models.CASCADE, verbose_name=_("Work Place"))

    tech_field = models.CharField(
        max_length=500, null=True, blank=True, verbose_name=_("Technical Field"))

    insurance_list = models.SmallIntegerField(
        default=1, verbose_name=_("Insurance List"))

    organization = models.ForeignKey(
        'Organization', null=True, blank=True, verbose_name=_("Organization"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Company Profile")
        verbose_name_plural = _("Company Profiles")

    def __str__(self) -> str:
        return f"{self.title}- {self.user.national_code}"


class Organization(models.Model):
    DEFEND = 'defend'

    ORGANIZATION_CHOICES = [
        (DEFEND, _("Defend"))
    ]
    organization_title = models.CharField(
        choices=ORGANIZATION_CHOICES, default=DEFEND, max_length=50, blank=True, null=True, verbose_name=_("Organization Title")
    )
    custom_organization_title = models.CharField(
        max_length=50, blank=True, null=True,
        help_text=_(
            "Enter a custom organization title if none of the choices apply."), verbose_name=_("Other Organization Title")
    )

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    def __str__(self) -> str:
        return f"{self.custom_organization_title}" if self.custom_organization_title else f"{self.get_organization_title_display()}"


class City(models.Model):

    name = models.CharField(max_length=200, verbose_name=_('Name'))

    province = models.ForeignKey(
        'Province', related_name='cities', on_delete=models.CASCADE, default="", verbose_name=_('Province'))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")


class Province(models.Model):

    name = models.CharField(max_length=200, unique=True,
                            verbose_name=_('Name'))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Province")
        verbose_name_plural = _("Provinces")


class Institute(models.Model):

    title = models.CharField(max_length=250, verbose_name=_('Title'))

    province = models.ForeignKey(
        Province, on_delete=models.CASCADE, verbose_name=_('Province'))

    def __str__(self) -> str:
        return f"{self.title} , {self.province}"

    class Meta:
        verbose_name = _("Institute")
        verbose_name_plural = _("Institutes")
