from .models import AnalysisReport
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import AccountTurnOver, AnalysisReport, CalculatedData, FinancialAsset,  ProfitLossStatement, SoldProductFee, BalanceReport

# Register your models here.


class ProfitStatementInline(admin.StackedInline):
    model = ProfitLossStatement
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


class AccountTurnOverInline(admin.StackedInline):
    model = AccountTurnOver
    extra = 0
    min_num = 1
    max_num = 1


@admin.register(FinancialAsset)
class FinancialAssestModel(admin.ModelAdmin):
    list_display = ['company_title', 'year']
    inlines = [BalanceReportInline, ProfitStatementInline, SaledProductInline,
               AccountTurnOverInline]

    @admin.display(ordering='company_title')
    def company_title(self, financial_asset: FinancialAsset):
        return financial_asset.company.company_title
    company_title.short_description = _("Company Title")

    search_fields = ['company__company_title', 'year']
    # This will allow selection of multiple life cycles


@admin.register(CalculatedData)
class CalculatedDataAdmin(admin.ModelAdmin):
    pass


@admin.register(AnalysisReport)
class AnalysisReportAdmin(admin.ModelAdmin):
    pass
