from datetime import timedelta
import random


from django.contrib.auth.models import AbstractBaseUser as BaseUser, PermissionsMixin,Group
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models


from core.validators import phone_number_validator
from core.managers import UserManager




class User(BaseUser, PermissionsMixin):
    phone_number = models.CharField(
        max_length=11, unique=True, validators=[phone_number_validator],verbose_name=_("Phone Number"))
    national_code = models.CharField(max_length=11, unique=True,verbose_name=_("National Code"))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="custom_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="custom_user_set",
        related_query_name="user",
    )

    USERNAME_FIELD = 'national_code'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.phone_number}"

    def has_perm(self, perm, obj=None):

        if self.is_superuser:
            return True

        return self.user_permissions.filter(codename=perm).exists() or super().has_perm(perm, obj)

    def has_module_perms(self, app_label):

        if self.is_superuser:
            return True

        return self.user_permissions.filter(content_type__app_label=app_label).exists() or super().has_module_perms(app_label)

    @property
    def is_admin(self):
        return self.is_superuser

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class OTP(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='otps')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        
        return self.created_at >= timezone.now() - timedelta(minutes=3)

    def generate_otp(self):
        return f"{random.randint(100000, 999999):06}"

    def __str__(self):
        return f"OTP for {self.user.phone_number} - Code: {self.otp_code}"

    class Meta:
        verbose_name = _("OTP")
        verbose_name_plural = _("OTPs")

class City(models.Model):

    name = models.CharField(max_length=200, verbose_name=_('Name'))

    province = models.ForeignKey(
        'Province', related_name='cities', on_delete=models.CASCADE, default="", verbose_name=_('Province'))

    def __str__(self) -> str:
        return self.name

    class Meta:
        unique_together = [['name', 'province']]
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


class Service(models.Model):

    name = models.CharField(max_length=255, verbose_name=_("Service Name"))

    description = models.TextField(verbose_name=_("Service Description"))

    price = models.DecimalField(
        decimal_places=2, max_digits=20, verbose_name=_("Price"))

    service_active = models.BooleanField(
        default=False, verbose_name=_("Service Active"))

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __str__(self) -> str:
        return f"{self.name} › {self.description[:10]}"
