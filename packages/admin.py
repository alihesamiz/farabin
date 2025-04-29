from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from packages.models import Service, Package, Subscription


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    ordering = ("-is_active", "-name")
    list_editable = ("is_active",)


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "price",
        "is_active",
        "period")
    list_filter = ("is_active",)
    search_fields = ("name", "description")
    ordering = ("-is_active", "-price")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "company_title",
        "package",
        "purchase_date",
        "expires_at",)
    search_fields = ("user__phone_number", "package__name")
    ordering = ("-purchase_date",)

    def company_title(self, obj):
        return obj.user.company.company_title
    company_title.short_description = _("Company Title")
