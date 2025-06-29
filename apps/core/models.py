from datetime import timedelta
import random


from django.contrib.auth.models import (
    AbstractBaseUser as BaseUser,
    PermissionsMixin,
    Group,
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db import models


from apps.core import Validator as _validator  # noqa: F401
from apps.core.managers import UserManager


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name=_("تاریخ ایجاد"), auto_now_add=True)
    updated_at = models.DateTimeField(
        verbose_name=_("تاریخ بروزرسانی"), auto_now_add=True)

    class Meta:
        abstract = True


class User(BaseUser, PermissionsMixin):
    phone_number = models.CharField(
        max_length=11,
        unique=True,
        validators=[_validator.phone_number_model_regex_validator],
        verbose_name=_("Phone Number"),
    )
    national_code = models.CharField(
        max_length=11, unique=True, verbose_name=_("National Code")
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

    USERNAME_FIELD = "national_code"
    REQUIRED_FIELDS = ["phone_number"]

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

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class OTP(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="otps")
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
        unique_together = [["name", "province"]]
        verbose_name = _("City")
        verbose_name_plural = _("Cities")


class Province(models.Model):
    name = models.CharField(max_length=200, unique=True,
                            verbose_name=_("Name"))

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _("Province")
        verbose_name_plural = _("Provinces")


class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Service Name"))

    description = models.TextField(verbose_name=_("Service Description"))

    price = models.DecimalField(
        decimal_places=2, max_digits=20, verbose_name=_("Price")
    )

    service_active = models.BooleanField(
        default=False, verbose_name=_("Service Active")
    )

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __str__(self) -> str:
        return f"{self.name} › {self.description[:10]}"


class PackagePermission(models.Model):
    name = models.CharField(max_length=255, unique=True)
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    service = models.ManyToManyField(
        "packages.Service", blank=True, related_name="permissions"
    )
    package = models.ForeignKey(
        "packages.Package",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="permissions",
    )

    def __str__(self):
        return self.name


class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(PackagePermission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "permission")


class QuestionMetric(TimeStampedModel):
    question = models.ForeignKey(
        "QuestionChoice", on_delete=models.CASCADE, related_name="metric", verbose_name=_("سوال"))
    title = models.CharField(verbose_name=_("Title"), max_length=128)
    weight = models.DecimalField(verbose_name=_(
        "Weight"), max_digits=4, decimal_places=2)

    class Meta:
        verbose_name = _("شاخص سوال")
        verbose_name_plural = _("شاخص‌های سوالات")

    def __str__(self):
        return f"{self.title!s}"


class QuestionChoice(models.Model):
    question = models.ForeignKey(
        "Question", on_delete=models.CASCADE, related_name="choices", verbose_name=_("سوال")
    )
    answer = models.CharField(max_length=128, verbose_name=_("پاسخ"))
    points = models.IntegerField(verbose_name=_("امتیاز"))

    class Meta:
        verbose_name = _("گزینه‌ سوال")
        verbose_name_plural = _("گزینه‌های سوالات")

    def __str__(self):
        return f"{self.answer} ({self.points} امتیاز)"


class Question(TimeStampedModel):
    text = models.CharField(max_length=255, verbose_name=_("سوال"))

    class Meta:
        verbose_name = _("سوال")
        verbose_name_plural = _("سوالات")

    def __str__(self):
        return f"{self.text!s}"


class Questionnaire(TimeStampedModel):
    name = models.CharField(max_length=255, verbose_name=_("عنوان"))
    questions = models.ManyToManyField(
        Question, through="QuestionnaireQuestion", verbose_name=_("سوالات")
    )

    class Meta:
        verbose_name = _("پرسشنامه")
        verbose_name_plural = _("پرسشنامه‌ها")

    def __str__(self):
        return f"{self.name!s}"


class QuestionnaireQuestion(TimeStampedModel):
    questionnaire = models.ForeignKey(
        Questionnaire, on_delete=models.CASCADE, verbose_name=_("پرسشنامه"))
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, verbose_name=_("سوال"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("عدد ترتیب"))

    class Meta:
        verbose_name = _("سوال پرسشنامه")
        verbose_name_plural = _("سوالات پرسشنامه‌ها")
        constraints = [
            models.UniqueConstraint(
                fields=["questionnaire", "question"],
                name="unique_questionnaire_question"
            )
        ]
        ordering = ['order']
