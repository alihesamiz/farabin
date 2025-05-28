from django.core.validators import MinValueValidator
import decimal


from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.db.transaction import atomic
from django.utils import timezone
from django.db import models

from django_lifecycle.conditions import WhenFieldValueIs, WhenFieldValueChangesTo
from django_lifecycle.hooks import AFTER_UPDATE, BEFORE_CREATE, BEFORE_UPDATE
from django_lifecycle.mixins import LifecycleModelMixin
from django_lifecycle.decorators import hook

User = get_user_model()


class PeriodChoices(models.TextChoices):
    MONTHLY = "monthly", _("ماهانه")
    QUARTERLY = "quarterly", _("سه ماهه")
    SEMI_ANNUALLY = "semi_annually", _("شش ماهه")
    ANNUALLY = "annually", _("سالانه")


class Service(LifecycleModelMixin, models.Model):
    class ServiceType(models.TextChoices):
        FINANCIAL = "financial", _("مالی")
        MARKETING = "marketing", _("بازاریابی")
        MANAGEMENT = "management", _("مدیریت")
        PRODUCTION = "production", _("ساخت و تولید")
        MIS = "mis", _("مدیریت سامانه اطلاعاتی")
        REASEARCH_AND_DEVELOPMENT = "research_and_development", _("تحقیق و توسعه")

    name = models.CharField(
        verbose_name=_("نام"),
        max_length=30,
        choices=ServiceType.choices,
        unique=True,
    )
    code_name = models.CharField(
        verbose_name=_("کد"), blank=True, max_length=2, unique=True
    )
    description = models.TextField(verbose_name=_("شرح سرویس"))
    price = models.DecimalField(
        decimal_places=2, max_digits=20, verbose_name=_("قیمت"), blank=True, null=True
    )
    period = models.CharField(
        max_length=20,
        choices=PeriodChoices.choices,
        verbose_name=_("دوره زمانی"),
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=False, verbose_name=_("فعال"))

    class Meta:
        verbose_name = _("سرویس")
        verbose_name_plural = _("سرویس‌ها")

    def __str__(self) -> str:
        return self.get_name_display()

    @hook(BEFORE_CREATE)
    def set_default_period(self):
        """
        Hook to set the default period of the services
        """
        with atomic():
            self.period = PeriodChoices.MONTHLY
            self.code_name = self.__get_code_name(self.name)

    def __get_code_name(self, service_name: str):
        for index, choice in enumerate(Service.ServiceType.choices):
            if service_name == choice[0]:
                return index


class Package(LifecycleModelMixin, models.Model):
    class PackageName(models.TextChoices):
        DEMO = "demo", _("آزمایشی")
        BRONZE = "bronze", _("برنزی")
        SILVER = "silver", _("نقره‌ای")
        GOLD = "gold", _("طلایی")
        PLATINUM = "platinum", _("پلاتینیوم")

    name = models.CharField(
        max_length=30,
        verbose_name=_("نام"),
        unique=True,
        choices=PackageName.choices,
    )
    code_name = models.CharField(
        verbose_name=_("کد"), blank=True, max_length=2, unique=True
    )
    description = models.TextField(verbose_name=_("شرح بسته"), blank=True, null=True)
    services = models.ManyToManyField(
        Service, verbose_name=_("سرویس"), related_name="packages", blank=True
    )
    price = models.DecimalField(
        decimal_places=2, max_digits=20, verbose_name=_("قیمت"), blank=True
    )
    period = models.CharField(
        max_length=20,
        choices=PeriodChoices.choices,
        verbose_name=_("دوره زمانی"),
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=False, verbose_name=_("فعال"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ایجاد"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("تاریخ بروزرسانی"))

    class Meta:
        verbose_name = _("بسته")
        verbose_name_plural = _("بسته‌ها")

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
        verbose_name=_("کاربر"),
    )
    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="subscriptions",
        null=True,
        blank=True,
        verbose_name=_("بسته"),
    )
    service = models.ManyToManyField(
        Service, related_name="subscriptions", blank=True, verbose_name=_("سرویس")
    )
    purchase_date = models.DateTimeField(
        auto_now_add=True, verbose_name=_("تاریخ خرید")
    )
    expires_at = models.DateTimeField(
        verbose_name=_("تاریخ انقضا"), blank=True, null=True
    )
    duration = models.DurationField(
        help_text=_("بازه زمانی به روز"),
        verbose_name=_("بازه زمانی"),
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True, verbose_name=_("فعال"))

    class Meta:
        verbose_name = _("اشتراک")
        verbose_name_plural = _("اشتراک‌ها")
        constraints = [
            models.UniqueConstraint(
                fields=["user", "package"], name="unique_user_package"
            ),
            # models.UniqueConstraint(
            #     fields=["user", "service"], name="unique_user_service"
            # )
        ]

    def __str__(self):
        return f"{self.user.company.company_title} - روز{self.duration.days}"

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
    coupon = models.CharField(verbose_name=_("کد تخفیف"), max_length=10, unique=True)
    discount = models.DecimalField(
        verbose_name=_("تخفیف"), max_digits=4, decimal_places=2
    )
    validated_from = models.DateTimeField(verbose_name=_("معتبر از"), auto_now_add=True)
    validated_until = models.DateTimeField(
        verbose_name=_("معتبر تا"), null=True, blank=True
    )
    available_for = models.SmallIntegerField(
        verbose_name=_("تعداد قابل استفاده"),
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    is_active = models.BooleanField(verbose_name=_("فعال است"), default=False)

    class Meta:
        verbose_name = _("تخفیف")
        verbose_name_plural = _("تخفیف‌ها")

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
        PENDING_STATUS = "pending", _("در انتظار")
        PAID_STATUS = "paid", _("پرداخت شده")
        CONFIRMED_STATUS = "confirmed", _("تایید شده")
        CANCELED_STATUS = "canceled", _("لغو شده")

    status = models.CharField(
        verbose_name=_("وضعیت"),
        choices=OrderStatus.choices,
        max_length=10,
        default=OrderStatus.PENDING_STATUS,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_("کاربر"), related_name="order"
    )
    package = models.ForeignKey(
        Package,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("بسته"),
        related_name="order",
    )
    service = models.ManyToManyField(
        Service, related_name="orders", blank=True, verbose_name=_("سرویس")
    )
    coupon = models.ForeignKey(
        Promotion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("کد تخفیف"),
    )

    created_at = models.DateTimeField(verbose_name=_("تاریخ ایجاد"), auto_now_add=True)

    class Meta:
        verbose_name = _("سفارش")
        verbose_name_plural = _("سفارش‌ها")
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
            getattr(self.user.company, "company_title", None)
            if hasattr(self.user, "company")
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
