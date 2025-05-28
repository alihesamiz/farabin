from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib import admin

from apps.packages.models import Order, Promotion, Service, Package, Subscription


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "price", "period", "is_active"]
    list_filter = ["is_active", "period"]
    search_fields = ["name", "description"]
    ordering = ["-is_active", "-name"]
    list_editable = [
        "is_active",
    ]


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
        "services_name",
        "price",
        "period",
        "is_active",
    ]
    search_fields = [
        "name",
        "description",
    ]
    ordering = ["-is_active", "-price"]
    filter_horizontal = ["services"]
    list_filter = ["is_active", "period"]

    @admin.display(description=_("Services"))
    def services_name(self, obj: Package):
        return ", ".join(s.__str__() for s in obj.services.all())


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = [
        "company_title",
        "package",
        "services",
        "purchase_date",
        "expires_at",
    ]
    search_fields = [
        "user__phone_number",
        "user__company__company_title",
        "package__name",
    ]
    ordering = [
        "-purchase_date",
    ]
    readonly_fields = [
        "duration",
    ]
    filter_horizontal = [
        "service",
    ]
    list_filter = ["package", "service__name"]

    @admin.display(description=_("Services"))
    def services(self, obj: Subscription):
        return ", ".join(s.__str__() for s in obj.service.all())

    @admin.display(description=_("Company Title"))
    def company_title(self, obj: Subscription):
        return obj.user.company.company_title


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "company_title",
        "package",
        "services",
        "status",
        "coupon",
        "price",
        "total_price",
        "created_at",
    ]
    search_fields = (
        "user__phone_number",
        "user__company__company_title",
        "package__name",
        "status",
    )
    ordering = ("-created_at",)
    list_filter = (
        "status",
        "package__name",
        "status",
    )
    list_editable = [
        "status",
    ]
    filter_horizontal = ["service"]

    @admin.display(description=_("Company Title"))
    def company_title(self, obj: Order):
        return obj.user.company.company_title

    @admin.display(description=_("Services"))
    def services(self, obj: Order):
        return ", ".join(s.__str__() for s in obj.service.all())

    @admin.display(description=_("Price"))
    def price(self, obj: Order):
        if obj.package:
            return obj.package.price
        elif obj.service.all():
            return sum(s.price for s in obj.service.all())

    @admin.display(description=_("قیمت کلی"))
    def total_price(self, obj: Order):
        return obj.total_price


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = [
        "coupon",
        "discount",
        "validated_from",
        "validated_until",
        "duration",
        "available_for",
        "is_active",
        "is_available",
    ]

    actions = ["deactivate", "activate"]

    @admin.display(description=_("قابل دسترس است"), boolean=True)
    def is_available(self, obj: Promotion):
        return obj.is_available

    @admin.display(description=_("بازه زمانی"))
    def duration(self, obj: Promotion):
        return obj.duration if obj.duration != float("inf") else "بدون زمان"

    @admin.action(description=_("غیرفعال کردن تخفیف"))
    def deactivate(self, request, queryset: Promotion):
        updated_count = queryset.update(is_active=False)
        self.message_user(
            request,
            _("{}کد تخفیف غیرفعال شد(ند).").format(updated_count),
            messages.SUCCESS,
        )

    @admin.action(description=_("فعال کردن تخفیف"))
    def activate(self, request, queryset: Promotion):
        updated_count = queryset.update(is_active=True)
        self.message_user(
            request,
            _("{}کد تخفیف فعال شد(ند).").format(updated_count),
            messages.SUCCESS,
        )
