from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import AccountTurnOver, FinancialAsset,  ProfitLossStatement, SoldProductFee, BalanceReport, TaxDeclarationFile

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
