from django.contrib import admin  # type: ignore
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _  # type: ignore

from apps.core.models import (
    OTP,
    User,
)


@admin.register(OTP)
class OtpAdmin(admin.ModelAdmin):
    list_display = ["user", "otp_code", "created_at"]


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "phone_number",
        "social_code",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = ("phone_number", "social_code")

    ordering = ("phone_number",)

    fieldsets = (
        (
            _("Personal info"),
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "avatar",
                    "social_code",
                    "phone_number",
                    "password",
                ]
            },
        ),
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
                    "social_code",
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
