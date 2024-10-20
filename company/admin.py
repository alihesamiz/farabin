from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import CompanyProfile, CompanyService, Dashboard
# Register your models here.


@admin.register(CompanyProfile)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_title', 'national_code',
                    'manager_name', 'tech_field', 'insurance_list']

    readonly_fields = ['id']

    @admin.display(ordering='national_code')
    def national_code(self, company_profile: CompanyProfile):
        return company_profile.user.national_code
    national_code.short_description = _("National Code")


@admin.register(CompanyService)
class CompanyServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    pass
