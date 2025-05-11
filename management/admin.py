from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from management.models import (
    HumanResource,
    PersonelInformation,
    OrganizationChartBase,
    SWOTAnalysis,
    SWOTQuestion,
    SWOTOption,
    SWOTMatrix,
)


@admin.register(PersonelInformation)
class PersonelInformationAdmin(admin.ModelAdmin):
    list_display = ["human_resource", "name", "obligations", "position"]
    autocomplete_fields = ["human_resource"]
    filter_horizontal = ["reports_to", "cooperates_with"]
    search_fields = ["name", "obligations", "position", "reports_to", "cooperates_with"]
    list_filter = [
        "human_resource",
        "obligations",
        "position",
        "reports_to",
        "cooperates_with",
    ]


@admin.register(HumanResource)
class HumanResourceAdmin(admin.ModelAdmin):
    list_display = ["company", "excel_file", "created_at", "updated_at"]
    autocomplete_fields = ["company"]
    search_fields = ["company", "excel_file"]
    list_filter = ["company", "created_at", "updated_at"]


@admin.register(OrganizationChartBase)
class OrganizationChartAdmin(admin.ModelAdmin):
    list_display = ["field", "position_excel"]
    search_fields = ["field", "position_excel"]
    list_filter = ["field", "position_excel"]


@admin.register(SWOTQuestion)
class SWOTQuestionAdmin(admin.ModelAdmin):
    list_display = ["text", "category"]
    search_fields = ["text", "category"]
    list_filter = ["category"]
    list_per_page = 20


@admin.register(SWOTOption)
class SWOTOptionAdmin(admin.ModelAdmin):
    list_display = [
        "company_name",
        "question",
        "answer",
        "category",
        "external_factor",
        "created_at",
        "updated_at",
    ]
    list_filter = ["company__company_title", "category"]
    search_fields = ["company__company_title", "answer"]
    list_per_page = 20

    @admin.display(
        description=_("Company Title"),
    )
    def company_name(self, obj):
        return obj.company.company_title


@admin.register(SWOTMatrix)
class SWOTMatrixAdmin(admin.ModelAdmin):
    list_display = ["company_name", "created_at", "updated_at"]
    filter_horizontal = ["options"]
    list_per_page = 20

    @admin.display(
        description=_("Company Title"),
    )
    def company_name(self, obj):
        return obj.company.company_title

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "options":
            if request.user.is_superuser:
                kwargs["queryset"] = SWOTOption.objects.all()
            else:
                kwargs["queryset"] = SWOTOption.objects.filter(
                    company__user=request.user
                )
        return super().formfield_for_manytomany(db_field, request, **kwargs)


@admin.register(SWOTAnalysis)
class SWOTAnalysisAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "created_at",
        "updated_at",
    ]
    list_filter = [
        "created_at",
        "updated_at",
    ]
    list_per_page = 20
