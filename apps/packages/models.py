import decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.transaction import atomic
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_lifecycle.conditions import WhenFieldValueChangesTo, WhenFieldValueIs
from django_lifecycle.decorators import hook
from django_lifecycle.hooks import AFTER_UPDATE, BEFORE_CREATE, BEFORE_UPDATE
from django_lifecycle.mixins import LifecycleModelMixin

User = get_user_model()


class PeriodChoices(models.TextChoices):
    MONTHLY = "monthly", _("Monthly")
    QUARTERLY = "quarterly", _("Quarterly")
    SEMI_ANNUALLY = "semi_annually", _("Semi-Annually")
    ANNUALLY = "annually", _("Annually")


class Service(LifecycleModelMixin, models.Model):
    class ServiceType(models.TextChoices):
        FINANCIAL = "financial", _("Financial")
        MARKETING = "marketing", _("Marketing")
        MANAGEMENT = "management", _("Management")
        PRODUCTION = "production", _("Production")
        MIS = "mis", _("Management Information System")
        RESEARCH_AND_DEVELOPMENT = (
            "research_and_development",
            _("Research and Development"),
        )

    name = models.CharField(
        verbose_name=_("Name"),
        max_length=30,
        choices=ServiceType.choices,
        unique=True,
    )
    code_name = models.CharField(
        verbose_name=_("Code"), blank=True, max_length=2, unique=True
    )
    description = models.TextField(verbose_name=_("Service Description"))
    price = models.DecimalField(
        decimal_places=2, max_digits=20, verbose_name=_("Price"), blank=True, null=True
    )
    period = models.CharField(
        max_length=20,
        choices=PeriodChoices.choices,
        verbose_name=_("Period"),
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=False, verbose_name=_("Active"))

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")

    def __str__(self) -> str:
        return self.get_name_display()

    @hook(BEFORE_CREATE)
    def set_default_period(self):
        """
        Hook to set the default period of the services
        """
        with atomic():
            self.period = PeriodChoices.MONTHLY
            # self.code_name = self.__get_code_name(self.name)

    # def __get_code_name(self, package_name: str):
    #     return self.PackageName.values.index(package_name)


# class UserModulePermission(models.Model):
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="module_permission",
#         verbose_name=_("User"),
#     )
#     company = models.ForeignKey(
#         "company.CompanyProfile",
#         on_delete=models.CASCADE,
#         related_name="module_permission",
#         verbose_name=_("Company"),
#     )
#     module = models.ForeignKey(
#         ServiceModule,
#         verbose_name=_("Module"),
#         on_delete=models.CASCADE,
#         related_name="module_permission",
#     )
#     can_access = models.BooleanField(default=False, verbose_name=_("Can Access"))

#     def __str__(self):
#         return f"Company({self.company.title}) user({self.user.phone_number}) access to module: {self.module.name}"

#     class Meta:
#         verbose_name = _("User module permission")
#         verbose_name_plural = _("User module permissions")
#         constraints = [
#             models.UniqueConstraint(
#                 name="unique_user_company_module_permission",
#                 fields=[
#                     "user",
#                     "company",
#                     "module",
#                 ],
#             )
#         ]


# class PackagePermission(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     codename = models.CharField(max_length=100, unique=True)
#     description = models.TextField(blank=True)
#     service = models.ManyToManyField(
#         "packages.Service", blank=True, related_name="permissions"
#     )
#     package = models.ForeignKey(
#         "packages.Package",
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name="permissions",
#     )

#     def __str__(self):
#         return self.name


# class UserPermission(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     permission = models.ForeignKey(PackagePermission, on_delete=models.CASCADE)

#     class Meta:
#         unique_together = ("user", "permission")


class Package(LifecycleModelMixin, models.Model):
    class PackageName(models.TextChoices):
        DEMO = "demo", _("Demo")
        BRONZE = "bronze", _("Bronze")
        SILVER = "silver", _("Silver")
        GOLD = "gold", _("Gold")
        PLATINUM = "platinum", _("Platinum")

    name = models.CharField(
        max_length=30,
        verbose_name=_("Name"),
        unique=True,
        choices=PackageName.choices,
    )
    code_name = models.CharField(
        verbose_name=_("Code"), blank=True, max_length=2, unique=True
    )
    description = models.TextField(
        verbose_name=_("Package Description"), blank=True, null=True
    )
    services = models.ManyToManyField(
        Service, verbose_name=_("Service"), related_name="packages", blank=True
    )
    price = models.DecimalField(
        decimal_places=2, max_digits=20, verbose_name=_("Price"), blank=True
    )
    period = models.CharField(
        max_length=20,
        choices=PeriodChoices.choices,
        verbose_name=_("Period"),
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=False, verbose_name=_("Active"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Package")
        verbose_name_plural = _("Packages")

    def __str__(self):
        return self.get_name_display()

    @hook(BEFORE_CREATE, condition=WhenFieldValueIs("name", PackageName.DEMO))
    def set_default_period(self):
        """
        Hook to set the default period of the package
        """
        with atomic():
            self.period = PeriodChoices.MONTHLY
            self.price = decimal.Decimal(0.00)
            self.code_name = self.__get_code_name(self.name)

    def __get_code_name(self, package_name: str):
        for index, choice in enumerate(self.PackageName.choices):
            if package_name == choice[0]:
                return index


class Subscription(LifecycleModelMixin, models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        verbose_name=_("User"),
    )
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        null=True,
        blank=True,
        verbose_name=_("Package"),
    )
    service = models.ManyToManyField(
        Service, related_name="subscriptions", blank=True, verbose_name=_("Service")
    )
    purchase_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Purchase Date")
    )
    expires_at = models.DateTimeField(
        verbose_name=_("Expiration Date"), blank=True, null=True
    )
    duration = models.DurationField(
        help_text=_("Time span in days"),
        verbose_name=_("Duration"),
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))

    class Meta:
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")
        constraints = [
            models.UniqueConstraint(
                fields=["user", "package"], name="unique_user_package"
            ),
            # models.UniqueConstraint(
            #     fields=["user", "service"], name="unique_user_service"
            # )
        ]

    def __str__(self):
        return f"{self.user.company.title} - {self.duration.days} days"

    @hook(BEFORE_CREATE)
    def manage_subscription(self):
        with atomic():
            now = timezone.now()
            self.purchase_date = now
            if self.package:
                self.duration = self._calculate_duration(self.package.period)
                self.expires_at = now + self.duration

    def _calculate_duration(self, period):
        match period:
            case PeriodChoices.MONTHLY:
                return timezone.timedelta(days=30)
            case PeriodChoices.QUARTERLY:
                return timezone.timedelta(days=90)
            case PeriodChoices.SEMI_ANNUALLY:
                return timezone.timedelta(days=180)
            case PeriodChoices.ANNUALLY:
                return timezone.timedelta(days=365)
            case _:
                raise ValueError("Invalid period")


class Promotion(LifecycleModelMixin, models.Model):
    coupon = models.CharField(verbose_name=_("Coupon Code"), max_length=10, unique=True)
    discount = models.DecimalField(
        verbose_name=_("Discount"), max_digits=4, decimal_places=2
    )
    validated_from = models.DateTimeField(
        verbose_name=_("Valid From"), auto_now_add=True
    )
    validated_until = models.DateTimeField(
        verbose_name=_("Valid Until"), null=True, blank=True
    )
    available_for = models.SmallIntegerField(
        verbose_name=_("Available Uses"),
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    is_active = models.BooleanField(verbose_name=_("Is Active"), default=False)

    class Meta:
        verbose_name = _("Promotion")
        verbose_name_plural = _("Promotions")

    def __str__(self):
        return f"{self.coupon!r}, {self.discount}%"

    @hook(BEFORE_CREATE)
    def set_discount_as_percentage(self):
        self.discount = self.discount / 100

    @property
    def duration(self):
        if self.validated_until:
            return self.validated_until - self.validated_from
        return float("inf")

    @property
    def is_available(self):
        return (
            self.available_for > 0
            and self.is_active
            and (not self.validated_until or self.validated_until > timezone.now())
        )

    def decrease_availability(self):
        if self.is_available:
            self.available_for -= 1
            self.save(update_fields=["available_for"])
            return True
        return False


class Order(LifecycleModelMixin, models.Model):
    class OrderStatus(models.TextChoices):
        PENDING_STATUS = "pending", _("Pending")
        PAID_STATUS = "paid", _("Paid")
        CONFIRMED_STATUS = "confirmed", _("Confirmed")
        CANCELED_STATUS = "canceled", _("Canceled")

    status = models.CharField(
        verbose_name=_("Status"),
        choices=OrderStatus.choices,
        max_length=10,
        default=OrderStatus.PENDING_STATUS,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("User"), related_name="order"
    )
    package = models.ForeignKey(
        Package,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Package"),
        related_name="order",
    )
    service = models.ManyToManyField(
        Service, related_name="orders", blank=True, verbose_name=_("Service")
    )
    coupon = models.ForeignKey(
        Promotion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Coupon"),
    )

    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")
        constraints = [
            models.UniqueConstraint(
                fields=["user", "package"], name="unique_user_package_order"
            ),
            # models.UniqueConstraint(
            #     fields=["user","service"],name="unique_user_service_order"
            # ),
            models.UniqueConstraint(
                fields=["user", "coupon"], name="unique_user_order_coupon"
            ),
        ]

    def __str__(self):
        user_info = (
            getattr(self.user.company_user.company, "title", None)
            if hasattr(self.user.company_user, "company")
            else self.user.phone_number
        )
        return f"{user_info} -> {self.created_at} : {self.get_status_display()}"

    @hook(AFTER_UPDATE, condition=WhenFieldValueIs("status", OrderStatus.PAID_STATUS))
    def create_subscription_of_confirmed_order(self):
        """
        Hook to create a subscription for the order if it is confirmed.
        """
        with atomic():
            subscription, created = Subscription.objects.get_or_create(
                user=self.user, package=self.package
            )

            if not subscription.purchase_date:
                subscription.purchase_date = timezone.now()

            if self.service.exists():
                subscription.service.set(self.service.all())

                [
                    duration := subscription._calculate_duration(ser.period)
                    for ser in subscription.service.all()
                ]
                expires_at = subscription.purchase_date + duration
                Subscription.objects.filter(pk=subscription.pk).update(
                    duration=duration, expires_at=expires_at
                )

            Order.objects.filter(pk=self.pk).update(
                status=Order.OrderStatus.CONFIRMED_STATUS
            )

    @hook(
        BEFORE_UPDATE,
        condition=WhenFieldValueChangesTo("status", OrderStatus.PAID_STATUS),
    )
    def set_as_paid(self):
        with atomic():
            if self.coupon and self.coupon.is_available:
                self.coupon.decrease_availability()

    @classmethod
    def get_by_status(cls, status, user=None):
        qs = cls.objects.filter(status=status)
        return qs.filter(user=user) if user else qs

    @property
    def total_price(self):
        price = sum(
            [item.price for item in [self.package] + list(self.service.all()) if item]
        )

        if self.coupon and self.coupon.is_available:
            discount_value = decimal.Decimal(1) - (self.coupon.discount)
            return price * discount_value
        return price
