from django.contrib import admin

from apps.management.models import (
    HumanResource,
    OrganizationChartBase,
    PersonelInformation,
    Position,
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


@admin.register(Position)
class PostitionAdmin(admin.ModelAdmin):
    list_display = ["code", "position"]
    search_fields = ["code", "position"]


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
