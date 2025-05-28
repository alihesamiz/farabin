from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib import admin


from apps.core.models import PackagePermission, Service, OTP, UserPermission


User = get_user_model()


@admin.register(OTP)
class OtpAdmin(admin.ModelAdmin):
    list_display = ["user", "otp_code", "created_at"]


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "phone_number",
        "national_code",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = ("phone_number", "national_code")

    ordering = ("phone_number",)

    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        (_("Personal info"), {"fields": ("national_code",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "national_code",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )

    readonly_fields = ("last_login", "password")

    filter_horizontal = ("groups", "user_permissions")

    list_filter = ("is_active", "is_staff", "is_superuser")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "get_price", "service_active"]

    def get_price(self, service: Service):
        return f"{service.price:,.2f}"

    get_price.short_description = _("Price")


@admin.register(PackagePermission)
class PackagePermissionAdmin(admin.ModelAdmin):
    list_display = ("name", "codename", "description")
    search_fields = ("name", "codename")


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ("user", "permission")
    list_filter = ("permission",)
    search_fields = ("user__username", "permission__name")
