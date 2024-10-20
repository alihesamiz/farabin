from django.contrib.auth.models import AbstractBaseUser as BaseUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models
from datetime import timedelta
import random
from .validators import phone_number_validator
from .managers import UserManager
# Create your models here.


class User(BaseUser):

    phone_number = models.CharField(
        max_length=11, unique=True, validators=[phone_number_validator])

    national_code = models.CharField(max_length=11, unique=True)

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


####################################
"""OTP Model"""


class OTP(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='+')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # OTP is valid for 10 minutes
        return self.created_at >= timezone.now() - timedelta(minutes=3)

    def generate_otp(self):
        return random.randint(100000, 999999)


####################################
"""Organizations Model"""


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


####################################
"""City and province Models"""


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


####################################
"""Work place Model"""


class Institute(models.Model):

    title = models.CharField(max_length=250, verbose_name=_('Title'))

    province = models.ForeignKey(
        Province, on_delete=models.CASCADE, verbose_name=_('Province'))

    def __str__(self) -> str:
        return f"{self.title} , {self.province}"

    class Meta:
        verbose_name = _("Institute")
        verbose_name_plural = _("Institutes")
