from .models import AnalysisReport
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import AccountTurnOver, AnalysisReport, FinancialData, FinancialAsset,  ProfitLossStatement, SoldProductFee, BalanceReport

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
    autocomplete_fields = ['company']
    list_display = ['company_title', 'year']
    inlines = [BalanceReportInline, ProfitStatementInline, SaledProductInline,
               AccountTurnOverInline]

    @admin.display(ordering='company_title')
    def company_title(self, financial_asset: FinancialAsset):
        return financial_asset.company.company_title
    company_title.short_description = _("Company Title")

    search_fields = ['company__company_title', 'year']
    # This will allow selection of multiple life cycles


@admin.register(FinancialData)
class CalculatedDataAdmin(admin.ModelAdmin):
    autocomplete_fields = ['financial_asset']
    list_display = ['company_title', 'financial_year']
    search_fields = [
        'financial_asset__company__company_title', 'financial_asset__year']

    def company_title(self, obj):
        return obj.financial_asset.company.company_title
    company_title.short_description = _('Company Title')  # Custom column name

    def financial_year(self, obj):
        return obj.financial_asset.year
    financial_year.short_description = _(
        'Year')  # Custom column name


@admin.register(AnalysisReport)
class AnalysisReportAdmin(admin.ModelAdmin):
    list_display = [
        "calculated_data",
        "chart_name",
        "text",
    ]
    autocomplete_fields = ['calculated_data']
    search_fields = [
        'calculated_data__financial_asset__company__company_title',]
