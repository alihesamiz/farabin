from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import BalanceReport, CompanyProfile, CompanyService, Dashboard, LifeCycle, TaxDeclaration
from diagnostics.models import SoldProductFee, ProfitLossStatement, FinancialAsset, BalanceReport
# Register your models here.


class LifeCycleInline(admin.StackedInline):
    model = LifeCycle
    extra = 0
    min_num = 1
    max_num = 1


class BalanceReprotInline(admin.TabularInline):
    model = BalanceReport
    extra = 0
    min_num = 1
    max_num = 1


@admin.register(LifeCycle)
class LifeCycleAdmin(admin.ModelAdmin):
    list_display = ['capital_providing',]


@admin.register(CompanyProfile)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_title', 'national_code', 'manager_name',
                    'tech_field', 'special_field_display', 'license', 'insurance_list', 'capital_providing_method_display']

    readonly_fields = ['id']

    filter_horizontal = ('capital_providing_method',)

    @admin.display(ordering='national_code')
    def national_code(self, company_profile: CompanyProfile):
        return company_profile.user.national_code
    national_code.short_description = _("National Code")

    def special_field_display(self, company_profile: CompanyProfile):
        return company_profile.special_field  # Ensure this matches the field name
    special_field_display.short_description = _("Special Field")

    @admin.display(description=_("Capital Providing Method"))
    def capital_providing_method_display(self, company_profile: CompanyProfile):
        return ", ".join([cycle.get_capital_providing_display() for cycle in company_profile.capital_providing_method.all()])


@admin.register(CompanyService)
class CompanyServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    pass


@admin.register(TaxDeclaration)
class TaxFileAdmin(admin.ModelAdmin):
    pass


@admin.register(BalanceReport)
class BalanceReportFileAdmin(admin.ModelAdmin):
    pass
