import random
from datetime import timedelta

from django.contrib.auth.models import (  # type: ignore
    AbstractBaseUser as BaseUser,
)
from django.contrib.auth.models import (
    Group,
    PermissionsMixin,
)
from django.db import models  # type: ignore
from django.utils import timezone  # type: ignore
from django.utils.translation import gettext_lazy as _  # type: ignore

from apps.core.managers import UserManager
from apps.core.utils import GeneralUtils
from constants.validators import Validator as _validator


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("Updated At"), auto_now=True)
    deleted_at = models.DateTimeField(
        verbose_name=_("Deleted At"), null=True, blank=True
    )

    class Meta:
        abstract = True


def get_user_avatar_path(instance, filename) -> str:
    return GeneralUtils(
        path="avatars", fields=["last_name", "first_name", "social_code"]
    ).rename_folder(instance, filename)

 
class User(BaseUser, PermissionsMixin):
    first_name = models.CharField(
        max_length=120,
        verbose_name=_("First name"),
        null=True,
        blank=True,
    )
    last_name = models.CharField(
        max_length=120,
        verbose_name=_("Last name"),
        null=True,
        blank=True,
    )
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        validators=[_validator.phone_number_model_regex_validator()],
        verbose_name=_("Phone Number"),
    )
    social_code = models.CharField(
        max_length=10, unique=True, verbose_name=_("Social Code")
    )
    avatar = models.ImageField(
        null=True,
        blank=True,
        verbose_name=_("Avatar"),
        upload_to=get_user_avatar_path,
        validators=[_validator.image_file_validator],
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="custom_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="custom_user_set",
        related_query_name="user",
    )

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["social_code"]

    objects = UserManager()

    def __str__(self) -> str:
        return f"{self.phone_number}"

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True

        return self.user_permissions.filter(codename=perm).exists() or super().has_perm(
            perm, obj
        )

    def has_module_perms(self, app_label):
        if self.is_superuser:
            return True

        return self.user_permissions.filter(
            content_type__app_label=app_label
        ).exists() or super().has_module_perms(app_label)

    @property
    def is_admin(self):
        return self.is_superuser

    @property
    def is_profile_complete(self):
        required_fields = [
            self.first_name,
            self.last_name,
            self.phone_number,
            self.social_code,
        ]
        return all(required_fields)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="otps")
    otp_code = models.CharField(max_length=6)
    is_active = models.BooleanField(default=True)
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
    name = models.CharField(max_length=200, verbose_name=_("Name"))

    province = models.ForeignKey(
        "Province",
        related_name="cities",
        on_delete=models.CASCADE,
        default="",
        verbose_name=_("Province"),
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
        constraints = [
            models.UniqueConstraint(
                name="unique_city_per_province",
                fields=[
                    "name",
                    "province",
                ],
            )
        ]


class Province(models.Model):
    name = models.CharField(max_length=200, unique=True, verbose_name=_("Name"))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Province")
        verbose_name_plural = _("Provinces")
