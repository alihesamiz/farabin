from .models import CompanyService, Service, Dashboard
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import CompanyProfile,  AccountTurnOver, FinancialAsset, LifeCycle, ProfitLossStatement, SoldProductFee, BalanceReport, TaxDeclarationFile

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



class ProfitStatementInline(admin.StackedInline):
    model = ProfitLossStatement
    extra = 0
    min_num = 1
    max_num = 1


class LifeCycleInline(admin.StackedInline):
    model = LifeCycle
    extra = 0
    min_num = 1
    max_num = 1


class SaledProductInline(admin.StackedInline):
    model = SoldProductFee
    extra = 0
    min_num = 1
    max_num = 1


class BalanceReportInline(admin.StackedInline):
    model = BalanceReport
    extra = 0
    min_num = 1
    max_num = 1


class TaxDeclarationInline(admin.StackedInline):
    model = TaxDeclarationFile
    extra = 0
    min_num = 1
    max_num = 1


class AccountTurnOverInline(admin.StackedInline):
    model = AccountTurnOver
    extra = 0
    min_num = 1
    max_num = 1


@admin.register(FinancialAsset)
class FinancialAssestModel(admin.ModelAdmin):
    list_display = ['company__company_title', 'year']
    inlines = [TaxDeclarationInline, BalanceReportInline, ProfitStatementInline, SaledProductInline,
               AccountTurnOverInline]
    # This will allow selection of multiple life cycles
    filter_horizontal = ('capital_providing_method',)


@admin.register(LifeCycle)
class LifeCycleAdmin(admin.ModelAdmin):
    list_display = ['capital_providing', 'other_capital_providing']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(CompanyService)
class CompanyServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(Dashboard)
class DashboardAdmin(admin.ModelAdmin):
    pass
