from django.contrib import admin

# Import all models
from apps.balancesheet.models.balance_sheet import *
from apps.balancesheet.models.contingent_account import *
from apps.balancesheet.models.current_asset import *
from apps.balancesheet.models.equity import *
from apps.balancesheet.models.expense import *
from apps.balancesheet.models.fixed_asset import *
from apps.balancesheet.models.long_term_liability import *
from apps.balancesheet.models.revenue import *
from apps.balancesheet.models.current_liability import *
from apps.balancesheet.models import *
from django import forms
import nested_admin
####


# ----------------------------- Inlines for CurrentAsset -----------------------------
class CashInline(nested_admin.NestedTabularInline):
    model = Cash

    extra = 1
    fields = (
        "id",
        "current_asset",
        "cash_in_hand", 
        "bank_balances", 
        "petty_cash", 
        "cash_in_transit"
        )


class ShortTermInvestmentInline(nested_admin.NestedTabularInline):
    model = ShortTermInvestment

    extra = 1
    can_add = False
    can_delete = True
    fields = (
        "id",
        "current_asset",
        "short_term_deposits",
        "tradable_stocks",
        "participation_bonds",
        "etf_investment_fund",
        "other_short_term_investments"

    )



class TradeReceivableInline(nested_admin.NestedTabularInline):
    model = TradeReceivable
 
    extra = 1
    fields = (
        "id",
        "current_asset",
        "trade_accounts_receivable",
        "trade_notes_receivable",
        "receivables_in_litigation",
        "notes_in_collection",
        "returned_cheques",
        "doubtful_receivables_provision",
    )

class NonTradeReceivableInline(nested_admin.NestedTabularInline):
    model = NonTradeReceivable
 
    extra = 1
    fields = (
        "id",
        "current_asset",
        "non_trade_accounts_receivable",
        "non_trade_notes_receivable",
        "employee_receivables",
        "director_receivables",
        "related_companies_receivables",
        "vat_receivable",
        "deposits_with_others",
        "dividends_receivable",
    )

class ShareholderReceivableInline(nested_admin.NestedTabularInline):
    model = ShareholderReceivable
 
    extra = 1
    fields = (
        "id",
        "current_asset",
        "amount",
    )

class InventoryInline(nested_admin.NestedTabularInline):
    model = Inventory
 
    extra = 1
    fields = (
        "id",
        "current_asset",
        "raw_materials",
        "work_in_progress",
        "finished_goods",
        "purchased_goods_for_sale",
        "spare_parts",
        "packaging_materials",
        "consignment_goods_with_others",
        "idle_items",
        "scrap_raw_materials",
        "inventory_impairment",
    )

class OrdersAndPrepaymentsInline(nested_admin.NestedTabularInline):
    model = OrdersAndPrepayments
 
    extra = 1
    fields = (
        "id",
        "current_asset",
        "prepaid_goods_and_services",
        "prepaid_income_tax",
        "prepaid_rent",
        "prepaid_insurance",
        "orders_in_transit",
        "prepaid_loans",
        "prepaid_interest_on_loans",
        "other_prepayments",
    )

class AssetsHeldForSaleInline(nested_admin.NestedTabularInline):
    model = AssetsHeldForSale
 
    extra = 1
    fields = (
        "id",
        "current_asset",
        "assets_held_for_sale",
        "impairment_reserve",
    )

class CurrentAssetInline(nested_admin.NestedTabularInline):
    model = CurrentAsset
    extra = 1
    fields = ("id", "balance_sheet")
    inlines = [
        CashInline,
        ShortTermInvestmentInline,
        TradeReceivableInline,
        NonTradeReceivableInline,
        ShareholderReceivableInline,
        InventoryInline,
        OrdersAndPrepaymentsInline,
        AssetsHeldForSaleInline,
    ]


# ----------------------------- Inlines for CurrentLiability -----------------------------
class TradeAccountsPayableInline(nested_admin.NestedTabularInline):
    model = TradeAccountsPayable
 
    extra = 1
    fields = (
        "id",
        "current_liability",
        "domestic_suppliers",
        "foreign_suppliers",
    )

class NonTradeAccountsPayableInline(nested_admin.NestedTabularInline):
    model = NonTradeAccountsPayable
 
    extra = 1
    fields = (
        "id",
        "current_liability",
        "salaries_payable",
        "social_security_payable",
        "deposits_from_entities",
        "deposits_from_individuals",
        "accrued_unpaid_expenses_provision",
    )

class ShareholderPayablesInline(nested_admin.NestedTabularInline):
    model = ShareholderPayables
 
    extra = 1
    fields = (
        "id",
        "current_liability",
        "amount",
    )

class DividendsPayableInline(nested_admin.NestedTabularInline):
    model = DividendsPayable
 
    extra = 1
    fields = (
        "id",
        "current_liability",
        "dividends_payable_to_individuals",
        "dividends_payable_to_shareholders",
        "dividends_payable_from_previous_years",
    )

class ShortTermLoansInline(nested_admin.NestedTabularInline):
    model = ShortTermLoans
 
    extra = 1
    fields = (
        "id",
        "current_liability",
        "loans_from_banks",
        "loans_from_individuals",
    )

class AdvancesAndDepositsInline(nested_admin.NestedTabularInline):
    model = AdvancesAndDeposits
 
    extra = 1
    fields = (
        "id",
        "current_liability",
        "advances_for_goods_sales",
        "advances_for_services",
        "advances_for_contracts",
        "deposits_from_others",
    )

class LiabilitiesRelatedToAssetsHeldForSaleInline(nested_admin.NestedTabularInline):
    model = LiabilitiesRelatedToAssetsHeldForSale
 
    extra = 1
    fields = (
        "id",
        "current_liability",
        "related_loans",
        "related_major_repairs_liability",
        "related_deferred_tax",
        "related_expert_fees_payable",
    )

class TaxProvisionInline(nested_admin.NestedTabularInline):
    model = TaxProvision
 
    extra = 1
    fields = (
        "id",
        "current_liability",
        "amount",
    )

class TaxPayableInline(nested_admin.NestedTabularInline):
    model = TaxPayable
 
    extra = 1
    fields = (
        "id",
        "current_liability",
        "payroll_tax",
        "withholding_tax",
        "vat_payable",
        "income_tax_payable",
    )

class CurrentLiabilityInline(nested_admin.NestedTabularInline):
    model = CurrentLiability
    extra = 1
    fields = ("id", "balance_sheet", "total_amount")
    inlines = [
        TradeAccountsPayableInline,
        NonTradeAccountsPayableInline,
        ShareholderPayablesInline,
        DividendsPayableInline,
        ShortTermLoansInline,
        AdvancesAndDepositsInline,
        LiabilitiesRelatedToAssetsHeldForSaleInline,
        TaxProvisionInline,
        TaxPayableInline,
    ]



# ----------------------------- Inlines for Equity -----------------------------
class InitialCapitalInline(nested_admin.NestedTabularInline):
    model = InitialCapital
 
    extra = 1
    fields = (
        "id",
        "equity",
        "amount",
    )

class CapitalIncreaseDecreaseInline(nested_admin.NestedTabularInline):
    model = CapitalIncreaseDecrease
 
    extra = 1
    fields = (
        "id",
        "equity",
        "amount",
    )

class SharePremiumReserveInline(nested_admin.NestedTabularInline):
    model = SharePremiumReserve
 
    extra = 1
    fields = (
        "id",
        "equity",
        "amount",
    )

class ShareDiscountReserveInline(nested_admin.NestedTabularInline):
    model = ShareDiscountReserve
 
    extra = 1
    fields = (
        "id",
        "equity",
        "amount",
    )

class LegalReserveInline(nested_admin.NestedTabularInline):
    model = LegalReserve
 
    extra = 1
    fields = (
        "id",
        "equity",
        "amount",
    )

class OtherReservesInline(nested_admin.NestedTabularInline):
    model = OtherReserves
 
    extra = 1
    fields = (
        "id",
        "equity",
        "amount",
    )

class RevaluationSurplusInline(nested_admin.NestedTabularInline):
    model = RevaluationSurplus
 
    extra = 1
    fields = (
        "id",
        "equity",
        "amount",
    )

class ForeignCurrencyTranslationDifferenceInline(nested_admin.NestedTabularInline):
    model = ForeignCurrencyTranslationDifference
 
    extra = 1
    fields = (
        "id",
        "equity",
        "amount",
    )

class RetainedEarningsInline(nested_admin.NestedTabularInline):
    model = RetainedEarnings
 
    extra = 1
    fields = (
        "id",
        "equity",
        "amount",
    )

class EquityInline(nested_admin.NestedTabularInline):
    model = Equity
    extra = 1
    fields = ("id", "balance_sheet", "total_amount")
    inlines = [
        InitialCapitalInline,
        CapitalIncreaseDecreaseInline,
        SharePremiumReserveInline,
        ShareDiscountReserveInline,
        LegalReserveInline,
        OtherReservesInline,
        RevaluationSurplusInline,
        ForeignCurrencyTranslationDifferenceInline,
        RetainedEarningsInline,
    ]




# ----------------------------- Inlines for Expense -----------------------------
class ProductionCostsInline(nested_admin.NestedTabularInline):
    model = ProductionCosts
 
    extra = 1
    fields = (
        "id",
        "expense",
        "direct_materials",
        "direct_labor",
        "machinery_depreciation",
        "production_line_insurance",
        "energy_and_fuel",
        "equipment_maintenance",
        "production_consumables",
        "production_rent",
        "raw_material_transport",
    )

class DistributionAndMarketingCostsInline(nested_admin.NestedTabularInline):
    model = DistributionAndMarketingCosts
 
    extra = 1
    fields = (
        "id",
        "expense",
        "marketing_salaries",
        "advertising_and_promotions",
        "warehousing_costs",
        "transportation_to_customers",
        "after_sales_services",
        "sales_commissions",
        "packaging_and_labeling",
        "exhibitions_and_events",
    )

class GeneralAndAdministrativeCostsInline(nested_admin.NestedTabularInline):
    model = GeneralAndAdministrativeCosts
 
    extra = 1
    fields = (
        "id",
        "expense",
        "administrative_salaries_payable",
        "head_office_rent",
        "utility_bills",
        "office_supplies",
        "administrative_assets_depreciation",
        "general_insurance",
        "audit_and_consulting_fees",
        "hospitality_and_transport",
    )

class FinancialCostsInline(nested_admin.NestedTabularInline):
    model = FinancialCosts
 
    extra = 1
    fields = (
        "id",
        "expense",
        "bank_interest_and_fees",
        "loan_late_penalties",
        "guarantee_fees",
        "discounting_expenses_on_receivables",
        "fund_transfer_and_bank_services",
    )

class OtherOperatingCostsInline(nested_admin.NestedTabularInline):
    model = OtherOperatingCosts
 
    extra = 1
    fields = (
        "id",
        "expense",
        "bad_debts_and_written_off_expense",
        "fx_non_operating_gain_loss",
        "impairment_short_term_investments",
        "inventory_write_down",
        "asset_impairment",
        "impairment_long_term_investments",
        "fx_operating_gain_loss",
    )

class ExpenseInline(nested_admin.NestedTabularInline):
    model = Expense
    extra = 1
    fields = ("id", "balance_sheet", "total_amount")
    inlines = [
        ProductionCostsInline,
        DistributionAndMarketingCostsInline,
        GeneralAndAdministrativeCostsInline,
        FinancialCostsInline,
        OtherOperatingCostsInline,
    ]



# ----------------------------- Inlines for FixedAsset -----------------------------
class IntangibleAssetInline(nested_admin.NestedTabularInline):
    model = IntangibleAsset
 
    extra = 1
    fields = (
        "id",
        "fixed_asset",
        "software",
        "royalty",
        "goodwill",
        "patent",
        "trademark",
        "copyright",
        "pre_operating_expenses",
    )

class TangibleFixedAssetInline(nested_admin.NestedTabularInline):
    model = TangibleFixedAsset
 
    extra = 1
    fields = (
        "id",
        "fixed_asset",
        "land",
        "building",
        "installations",
        "machinery_and_equipment",
        "vehicles",
        "office_furniture",
        "accumulated_depreciation",
    )

class AssetsInProgressInline(nested_admin.NestedTabularInline):
    model = AssetsInProgress
 
    extra = 1
    fields = (
        "id",
        "fixed_asset",
        "amount",
    )

class LongTermInvestmentInline(nested_admin.NestedTabularInline):
    model = LongTermInvestment
 
    extra = 1
    fields = (
        "id",
        "fixed_asset",
        "investment_in_affiliates",
        "investment_in_subsidiaries",
        "investment_in_private_companies",
        "long_term_bonds",
        "property_investment",
        "long_term_deposits",
        "long_term_participation_in_projects",
        "long_term_treasury_investment",
        "long_term_investment_impairment",
    )

class OtherNonCurrentAssetInline(nested_admin.NestedTabularInline):
    model = OtherNonCurrentAsset
 
    extra = 1
    fields = (
        "id",
        "fixed_asset",
        "amount",
    )

class FixedAssetInline(nested_admin.NestedTabularInline):
    model = FixedAsset
    extra = 1
    fields = ("id", "balance_sheet", "total_amount")
    inlines = [
        IntangibleAssetInline,
        TangibleFixedAssetInline,
        AssetsInProgressInline,
        LongTermInvestmentInline,
        OtherNonCurrentAssetInline,
    ]


# ----------------------------- Inlines for LongTermLiability -----------------------------
class LongTermAccountsPayableInline(nested_admin.NestedTabularInline):
    model = LongTermAccountsPayable
 
    extra = 1
    fields = (
        "id",
        "long_term_liability",
        "long_term_notes_payable",
        "long_term_accounts_payable",
    )

class LongTermLoansInline(nested_admin.NestedTabularInline):
    model = LongTermLoans
 
    extra = 1
    fields = (
        "id",
        "long_term_liability",
        "loans_from_banks",
    )

class LongTermProvisionsInline(nested_admin.NestedTabularInline):
    model = LongTermProvisions
 
    extra = 1
    fields = (
        "id",
        "long_term_liability",
        "employee_end_of_service_benefits",
    )

class LongTermLiabilityInline(nested_admin.NestedTabularInline):
    model = LongTermLiability
    extra = 1
    fields = ("id", "balance_sheet", "total_amount")
    inlines = [
        LongTermAccountsPayableInline,
        LongTermLoansInline,
        LongTermProvisionsInline,
    ]


# ----------------------------- Inlines for Revenue -----------------------------
class NetSalesInline(nested_admin.NestedTabularInline):
    model = NetSales
 
    extra = 1
    fields = (
        "id",
        "revenue",
        "amount",
    )

class ServiceRevenueInline(nested_admin.NestedTabularInline):
    model = ServiceRevenue
 
    extra = 1
    fields = (
        "id",
        "revenue",
        "amount",
    )

class ForeignCurrencyRevenueInline(nested_admin.NestedTabularInline):
    model = ForeignCurrencyRevenue
 
    extra = 1
    fields = (
        "id",
        "revenue",
        "amount",
    )

class OtherOperatingRevenueInline(nested_admin.NestedTabularInline):
    model = OtherOperatingRevenue
 
    extra = 1
    fields = (
        "id",
        "revenue",
        "amount",
    )

class RevenueInline(nested_admin.NestedTabularInline):
    model = Revenue
    extra = 1
    fields = ("id", "balance_sheet", "total_amount")
    inlines = [
        NetSalesInline,
        ServiceRevenueInline,
        ForeignCurrencyRevenueInline,
        OtherOperatingRevenueInline,
    ]



# # ----------------------------- Inlines for ContingentAccounts -----------------------------
# class ContingentCounterpartiesInline(nested_admin.NestedTabularInline):
#     model = ContingentCounterparties
#     extra = 1
#     fields = ("id", "contingent_account", "our_counterparties_with_others", "others_counterparties_with_us", "amount")

# class ContingentAccountsInline(nested_admin.NestedTabularInline):
#     model = ContingentAccounts
#     extra = 1
#     fields = ("id", "contingent_account", "our_accounts_with_others", "others_accounts_with_us", "total_contingent_accounts")
#     readonly_fields = ("total_contingent_accounts",)
#     inlines = [ContingentCounterpartiesInline]




# ----------------------------- Balance Sheet Admin -----------------------------
@admin.register(BalanceSheet)
class BalanceSheetAdmin(nested_admin.NestedModelAdmin):
    list_display = ("id", "company", "year", "created_at")
    inlines = [
        CurrentAssetInline,FixedAssetInline, CurrentLiabilityInline, LongTermLiabilityInline, EquityInline
        , RevenueInline, ExpenseInline, #ContingentAccountsInline, 
    ]   
