from uuid import uuid4
import decimal


from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from django.utils import timezone
from django.db import models


User = get_user_model()


class Service(models.Model):

    class ServiceType(models.TextChoices):
        FINANCIAL = "financial", _("Financial")
        MARKETING = "marketing", _("Marketing")
        MANAGEMENT = "management", _("Management")
        PRODUCTION = "production", _("Production")
        MIS = "mis", _("Management Information System")
        REASEARCH_AND_DEVELOPMENT = "research_and_development", _(
            "Research and Development")

    name = models.CharField(verbose_name=_(
        "Service Name"), max_length=30, choices=ServiceType.choices, unique=True)

    description = models.TextField(verbose_name=_("Service Description"))

    is_active = models.BooleanField(
        default=False, verbose_name=_("Is Active?"))

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __str__(self) -> str:
        return self.get_name_display()


class Package(models.Model):
    class PackageName(models.TextChoices):
        DEMO = "demo", _("Demo")
        BRONZE = "bronze", _("Bronze")
        SILVER = "silver", _("Silver")
        GOLD = "gold", _("Gold")
        PLATINUM = "platinum", _("Platinum")

    class PeriodChoices(models.TextChoices):
        MONTHLY = "monthly", _("Monthly")
        QUARTERLY = "quarterly", _("Quarterly")
        SEMI_ANNUALLY = "semi_annually", _("Semi-Annually")
        ANNUALLY = "annually", _("Annually")

    name = models.CharField(
        max_length=30, verbose_name=_("Package Name"), unique=True, choices=PackageName.choices)
    description = models.TextField(
        verbose_name=_("Package Description"), blank=True, null=True)
    services = models.ManyToManyField(
        Service, verbose_name=_("Services"), related_name="packages", blank=True)
    price = models.DecimalField(
        decimal_places=2, max_digits=20, verbose_name=_("Price"), blank=True)
    period = models.CharField(
        max_length=20, choices=PeriodChoices.choices,
        verbose_name=_("Period"), blank=True, null=True
    )
    is_active = models.BooleanField(
        default=False, verbose_name=_("Is Active?"))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Package")
        verbose_name_plural = _("Packages")

    def __str__(self):
        return self.get_name_display()

    def save(self, *args, **kwargs):
        not_created = self.pk is None
        with atomic():
            if not_created and self.name == self.PackageName.DEMO:
                self.period = self.PeriodChoices.MONTHLY
                self.price = decimal.Decimal(0.00)

            super().save(*args, **kwargs)


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriptions")
    package = models.ForeignKey(
        Package, on_delete=models.CASCADE, related_name="subscriptions")
    purchase_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Purchase Date"))
    expires_at = models.DateTimeField(
        verbose_name=_("Expiry Date"), blank=True, null=True)
    duration = models.DurationField(
        help_text=_("Duration in days"),
        verbose_name=_("Duration"), blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))

    class Meta:
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")
        unique_together = (
            "user", "package", "purchase_date"
        )

    def __str__(self):
        return f"{self.user.phone_number} - {self.package.name}({self.package.period})"

    def save(self, *args, **kwargs):
        # On first save, set expires_at based on package.duration
        if not self.pk:
            with atomic():
                now = timezone.now()
                self.purchase_date = now
                self.duration = self._calculate_duration()
                self.expires_at = now + self.duration
            super().save(*args, **kwargs)

    def _calculate_duration(self):

        match self.package.period:
            case Package.PeriodChoices.MONTHLY:
                return timezone.timedelta(days=30)
            case Package.PeriodChoices.QUARTERLY:
                return timezone.timedelta(days=90)
            case Package.PeriodChoices.SEMI_ANNUALLY:
                return timezone.timedelta(days=180)
            case Package.PeriodChoices.ANNUALLY:
                return timezone.timedelta(days=365)
            case _:
                raise ValueError("Invalid period")


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING_STATUS = 'pending', _('Pending')
        CONFIRMED_STATUS = 'confirmed', _('Confirmed')
        CANCELED_STATUS = 'canceled', _('Canceled')

    status = models.CharField(verbose_name=_(
        "Status"), choices=OrderStatus.choices, max_length=10, default=OrderStatus.PENDING_STATUS)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("User"), related_name="order")
    package = models.ForeignKey(Package, on_delete=models.SET_NULL,
                                null=True, verbose_name=_("Package"), related_name="order")
    created_at = models.DateTimeField(
        verbose_name=_("Created At"), auto_now_add=True)

    def __str__(self):
        user_info = (
            getattr(self.user.company, "company_title", None)
            if hasattr(self.user, "company") else self.user.phone_number
        )
        return f"{user_info} -> {self.created_at.date()} : {self.get_status_display()}"

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        constraints = [
            models.UniqueConstraint(
                fields=["user", "package"],
                name="user_unique_package_order")
        ]

    def set_as_paied(self):
        with atomic():
            self.status = self.OrderStatus.CONFIRMED_STATUS
            self.save()

    @classmethod
    def get_by_status(cls, status, user=None):
        qs = cls.objects.filter(status=status)
        return qs.filter(user=user) if user else qs
