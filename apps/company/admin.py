from django.utils.translation import gettext_lazy as _

# from django.contrib import messages
from django.contrib import admin


from apps.company.models import (
    CompanyProfile,
    CompanyUser,
    CompanyService,
    CompanyUserServicePermission,
    LifeCycle,
    License,
    LifeCycleFinancialResource,
    LifeCycleQuantitative,
    LifeCycleTheoretical,
    LifeCycleDecline,
    LifeCycleGrowth,
    LifeCycleIntroduction,
    LifeCycleMaturity,
    LifeCycleFeature,
)


class LifeCycleInline(admin.StackedInline):
    model = LifeCycle
    extra = 0
    min_num = 1
    max_num = 1


@admin.register(LifeCycle)
class LifeCycleAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "code",
    ]


@admin.register(CompanyProfile)
class CompanyAdmin(admin.ModelAdmin):
    search_fields = ["title"]
    list_display = [
        "title",
        "tech_field",
        "special_field_display",
        "insurance_list",
        # "capital_providing_method_display",
    ]

    readonly_fields = ["id"]

    filter_horizontal = ("capital_providing_method", "license")

    @admin.display(description=_("Special Field"))
    def special_field_display(self, company_profile: CompanyProfile):
        return company_profile.special_field

    # @admin.display(
    #     description=_("Capital Providing Method"),
    #     ordering="capital_providing_method_display",
    # )
    # def capital_providing_method_display(self, company_profile: CompanyProfile):
    #     return ", ".join(
    #         [
    #             cycle.get_capital_providing_display()
    #             for cycle in company_profile.capital_providing_method.all()
    #         ]
    #     )


@admin.register(LifeCycleFeature)
class LifeCycleFeatureAdmin(admin.ModelAdmin):
    list_display = ("name", "weight")
    search_fields = ("name",)
    list_filter = ("weight",)
    ordering = ("name",)
    list_per_page = 20


# Admin for LifeCycleDecline
@admin.register(LifeCycleDecline)
class LifeCycleDeclineAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 20


# Admin for LifeCycleMaturity
@admin.register(LifeCycleMaturity)
class LifeCycleMaturityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 20


# Admin for LifeCycleGrowth
@admin.register(LifeCycleGrowth)
class LifeCycleGrowthAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 20


# Admin for LifeCycleIntroduction
@admin.register(LifeCycleIntroduction)
class LifeCycleIntroductionAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 20


# Admin for LifeCyclePlace
@admin.register(LifeCycleTheoretical)
class LifeCyclePlaceAdmin(admin.ModelAdmin):
    list_display = (
        "company__title",
        "feature",
        "decline",
        "maturity",
        "growth",
        "introduction",
        "created_at",
        "updated_at",
    )
    list_filter = ("company", "created_at", "updated_at")
    search_fields = ("company__title", "feature__name")
    date_hierarchy = "created_at"
    list_per_page = 20
    ordering = ("-created_at",)
    autocomplete_fields = [
        "company",
        "feature",
        "decline",
        "maturity",
        "growth",
        "introduction",
    ]

    # Configure autocomplete search fields
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "company":
            kwargs["queryset"] = db_field.related_model.objects.all()
        elif db_field.name in [
            "feature",
            "decline",
            "maturity",
            "growth",
            "introduction",
        ]:
            kwargs["queryset"] = db_field.related_model.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(LifeCycleFinancialResource)
class LifeCycleFinancialResourceAdmin(admin.ModelAdmin): ...


@admin.register(LifeCycleQuantitative)
class LifeCycleQuantitaticeAdmin(admin.ModelAdmin):
    list_display = [
        "company__title",
        "resource_value",
        "created_at",
        "updated_at",
    ]
    filter_horizontal = ["resource"]

    @admin.display(description=_("چرخه عمر منابع مالی"))
    def resource_value(self, obj: LifeCycleQuantitative):
        return " | ".join(
            [resource.get_name_display() for resource in obj.resource.all()]
        )

    @admin.display(description=_("شرکت"))
    def company__title(self, obj: LifeCycleQuantitative):
        return obj.company.title



@admin.register(CompanyService)
class CompanyServiceAdmin(admin.ModelAdmin):
    list_display = [
        "company",
        "service",
        "is_active",
        "purchased_at",
        "deleted_at",
    ]


@admin.register(CompanyUser)
class CompanyUserAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "company",
        "role",
    ]


@admin.register(CompanyUserServicePermission)
class CompanyUserServicePermissionAdmin(admin.ModelAdmin):
    list_display = [
        "company_user",
        "service",
        "created_at",
        "updated_at",
        "deleted_at",
    ]
