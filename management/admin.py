from django.contrib import admin

from management.models import (HumanResource, PersonelInformation, OrganizationChartBase, SWOTAnalysis,
                               SWOTStrengthOption, SWOTWeaknessOption, SWOTOpportunityOption, SWOTThreatOption, SWOTMatrix
                               )


@admin.register(PersonelInformation)
class PersonelInformationAdmin(admin.ModelAdmin):
    list_display = ['human_resource', 'name',
                    'obligations', 'position']
    autocomplete_fields = ['human_resource']
    filter_horizontal = ['reports_to', 'cooperates_with']
    search_fields = ['name', 'obligations',
                     'position', 'reports_to', 'cooperates_with']
    list_filter = ['human_resource', 'obligations',
                   'position', 'reports_to', 'cooperates_with']


@admin.register(HumanResource)
class HumanResourceAdmin(admin.ModelAdmin):
    list_display = ['company', 'excel_file', 'created_at', 'updated_at']
    autocomplete_fields = ['company']
    search_fields = ['company', 'excel_file']
    list_filter = ['company', 'created_at', 'updated_at']


@admin.register(OrganizationChartBase)
class OrganizationChartAdmin(admin.ModelAdmin):
    list_display = ['field', 'position_excel']
    search_fields = ['field', 'position_excel']
    list_filter = ['field', 'position_excel']


class OptionsAdmin(admin.ModelAdmin):
    list_display = ['name', 'custom_name']
    search_fields = ['name', 'custom_name']
    list_filter = ['name',]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'name':
            kwargs['required'] = False
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(SWOTStrengthOption)
class StrengthAdmin(OptionsAdmin):
    ...


@admin.register(SWOTWeaknessOption)
class WeaknessAdmin(OptionsAdmin):
    ...


@admin.register(SWOTOpportunityOption)
class OpportunityAdmin(OptionsAdmin):
    ...


@admin.register(SWOTThreatOption)
class ThreatAdmin(OptionsAdmin):
    ...


@admin.register(SWOTMatrix)
class SWOTMatrixAdmin(admin.ModelAdmin):
    list_display = ['company',  'created_at']
    list_filter = ['created_at',]
    search_fields = ['company__company_title',]
    filter_horizontal = ['strengths', 'weaknesses', 'opportunities', 'threats']


@admin.register(SWOTAnalysis)
class SWOTAnalysisAdmin(admin.ModelAdmin):
    list_display = ['swot_matrix', 'is_approved']
    autocomplete_fields = ['swot_matrix']
    search_fields = ['swot_matrix', "company__company_title", "is_approved"]
