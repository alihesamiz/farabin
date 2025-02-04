from django.contrib import admin

from management.models import HumanResource, PersonelInformation,OrganizationChart

# Register your models here.




@admin.register(PersonelInformation)
class PersonelInformationAdmin(admin.ModelAdmin):
    list_display = ['human_resource', 'name', 'unit', 'position','reports_to']
    autocomplete_fields = ['human_resource']
    search_fields = ['name', 'unit', 'position','reports_to']
    list_filter = ['human_resource', 'unit', 'position','reports_to']
    
@admin.register(HumanResource)
class HumanResourceAdmin(admin.ModelAdmin):
    list_display = ['company', 'excel_file', 'create_at', 'updated_at']
    autocomplete_fields = ['company']
    search_fields = ['company', 'excel_file']
    list_filter = ['company', 'create_at', 'updated_at']

@admin.register(OrganizationChart)
class OrganizationChartAdmin(admin.ModelAdmin):
    list_display = ['position_excel']
    search_fields = ['position_excel']
    list_filter = ['position_excel']