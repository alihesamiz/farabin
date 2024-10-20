from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import AccountTurnOver, FinancialAsset, LifeCycle, ProfitLossStatement, SoldProductFee, BalanceReport, TaxDeclarationFile, Service

# Register your models here.


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
