from rest_framework import serializers
from apps.balancesheet.models.balance_sheet import BalanceSheet

from apps.balancesheet.models.contingent_account import (
    ContingentAccount,
    ContingentAccounts,
    ContingentCounterparties,
)
from apps.balancesheet.models.current_liability import (
    CurrentLiability,
    TradeAccountsPayable,
    NonTradeAccountsPayable,
    ShareholderPayables,
    DividendsPayable,
    ShortTermLoans,
    AdvancesAndDeposits,
    LiabilitiesRelatedToAssetsHeldForSale,
    TaxProvision,
    TaxPayable,
)

from apps.balancesheet.models.current_asset import (
    CurrentAsset,
    Cash,
    ShortTermInvestment,
    TradeReceivable,
    NonTradeReceivable,
    ShareholderReceivable,
    Inventory,
    OrdersAndPrepayments,
    AssetsHeldForSale,
)
from apps.balancesheet.models.long_term_liability import (
    LongTermLiability,
    LongTermAccountsPayable,
    LongTermLoans,
    LongTermProvisions,
)

from apps.balancesheet.models.equity import (
    Equity,
    InitialCapital,
    CapitalIncreaseDecrease,
    SharePremiumReserve,
    ShareDiscountReserve,
    LegalReserve,
    OtherReserves,
    RevaluationSurplus,
    ForeignCurrencyTranslationDifference,
    RetainedEarnings,
)

from apps.balancesheet.models.expense import (
    Expense,
    ProductionCosts,
    DistributionAndMarketingCosts,
    GeneralAndAdministrativeCosts,
    FinancialCosts,
    OtherOperatingCosts,
)

from apps.balancesheet.models.fixed_asset import (
    FixedAsset,
    IntangibleAsset,
    TangibleFixedAsset,
    AssetsInProgress,
    LongTermInvestment,
    OtherNonCurrentAsset,
)

from apps.balancesheet.models.revenue import (
    Revenue,
    NetSales,
    ServiceRevenue,
    ForeignCurrencyRevenue,
    OtherOperatingRevenue,
)

from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError


class BalanceSheetFileUploadSerializer(serializers.Serializer):
    model = BalanceSheet
    
    file = serializers.FileField()
    company_name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    year = serializers.IntegerField()
    file_path = serializers.CharField(max_length=500, required=False, allow_blank=True)


    permission_classes = [IsAuthenticated]  # Require authenticated user


    def validate_file(self, value):
            # Check file size (e.g., max 5MB)
            max_size = 5 * 1024 * 1024  # 5MB in bytes
            if value.size > max_size:
                raise ValidationError("File size exceeds 5MB limit.")
            # Check file type (e.g., allow only PDF)
            if not value.name.lower().endswith('.xlsx'):
                raise ValidationError("Only PDF files are allowed.")
            return value
































class BalanceSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceSheet
        fields = ['id', 'company', 'year']


class FixedAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FixedAsset
        fields = ['balance_sheet', 'total_amount']

class IntangibleAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntangibleAsset
        fields = [
            'fixed_asset',
            'software',
            'royalty',
            'goodwill',
            'patent',
            'trademark',
            'copyright',
            'pre_operating_expenses'
        ]

class TangibleFixedAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = TangibleFixedAsset
        fields = [
            'fixed_asset',
            'land',
            'building',
            'installations',
            'machinery_and_equipment',
            'vehicles',
            'office_furniture',
            'accumulated_depreciation'
        ]

class AssetsInProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetsInProgress
        fields = ['fixed_asset', 'amount']

class LongTermInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongTermInvestment
        fields = [
            'fixed_asset',
            'investment_in_affiliates',
            'investment_in_subsidiaries',
            'investment_in_private_companies',
            'long_term_bonds',
            'property_investment',
            'long_term_deposits',
            'long_term_participation_in_projects',
            'long_term_treasury_investment',
            'long_term_investment_impairment'
        ]

class OtherNonCurrentAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherNonCurrentAsset
        fields = ['fixed_asset', 'amount']

class CurrentLiabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentLiability
        fields = ['balance_sheet', 'total_amount']

class TradeAccountsPayableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeAccountsPayable
        fields = ['current_liability', 'domestic_suppliers', 'foreign_suppliers']

class NonTradeAccountsPayableSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonTradeAccountsPayable
        fields = [
            'current_liability',
            'salaries_payable',
            'social_security_payable',
            'deposits_from_entities',
            'deposits_from_individuals',
            'accrued_unpaid_expenses_provision'
        ]

class ShareholderPayablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareholderPayables
        fields = ['current_liability', 'amount']

class DividendsPayableSerializer(serializers.ModelSerializer):
    class Meta:
        model = DividendsPayable
        fields = [
            'current_liability',
            'dividends_payable_to_individuals',
            'dividends_payable_to_shareholders',
            'dividends_payable_from_previous_years'
        ]

class ShortTermLoansSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortTermLoans
        fields = ['current_liability', 'loans_from_banks', 'loans_from_individuals']

class AdvancesAndDepositsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvancesAndDeposits
        fields = [
            'current_liability',
            'advances_for_goods_sales',
            'advances_for_services',
            'advances_for_contracts',
            'deposits_from_others'
        ]

class LiabilitiesRelatedToAssetsHeldForSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LiabilitiesRelatedToAssetsHeldForSale
        fields = [
            'current_liability',
            'related_loans',
            'related_major_repairs_liability',
            'related_deferred_tax',
            'related_expert_fees_payable'
        ]

class TaxProvisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxProvision
        fields = ['current_liability', 'amount']

class TaxPayableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxPayable
        fields = [
            'current_liability',
            'payroll_tax',
            'withholding_tax',
            'vat_payable',
            'income_tax_payable'
        ]

class LongTermLiabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = LongTermLiability
        fields = ['balance_sheet', 'total_amount']

class LongTermAccountsPayableSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongTermAccountsPayable
        fields = ['long_term_liability', 'long_term_notes_payable', 'long_term_accounts_payable']

class LongTermLoansSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongTermLoans
        fields = ['long_term_liability', 'loans_from_banks']

class LongTermProvisionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LongTermProvisions
        fields = ['long_term_liability', 'employee_end_of_service_benefits']

class EquitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Equity
        fields = ['balance_sheet', 'total_amount']

class InitialCapitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = InitialCapital
        fields = ['equity', 'amount']

class CapitalIncreaseDecreaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CapitalIncreaseDecrease
        fields = ['equity', 'amount']

class SharePremiumReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharePremiumReserve
        fields = ['equity', 'amount']

class ShareDiscountReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareDiscountReserve
        fields = ['equity', 'amount']

class LegalReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalReserve
        fields = ['equity', 'amount']

class OtherReservesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherReserves
        fields = ['equity', 'amount']

class RevaluationSurplusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevaluationSurplus
        fields = ['equity', 'amount']

class ForeignCurrencyTranslationDifferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForeignCurrencyTranslationDifference
        fields = ['equity', 'amount']

class RetainedEarningsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetainedEarnings
        fields = ['equity', 'amount']

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['balance_sheet', 'total_amount']

class ProductionCostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionCosts
        fields = [
            'expense',
            'direct_materials',
            'direct_labor',
            'machinery_depreciation',
            'production_line_insurance',
            'energy_and_fuel',
            'equipment_maintenance',
            'production_consumables',
            'production_rent',
            'raw_material_transport'
        ]

class DistributionAndMarketingCostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DistributionAndMarketingCosts
        fields = [
            'expense',
            'marketing_salaries',
            'advertising_and_promotions',
            'warehousing_costs',
            'transportation_to_customers',
            'after_sales_services',
            'sales_commissions',
            'packaging_and_labeling',
            'exhibitions_and_events'
        ]

class GeneralAndAdministrativeCostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralAndAdministrativeCosts
        fields = [
            'expense',
            'administrative_salaries_payable',
            'head_office_rent',
            'utility_bills',
            'office_supplies',
            'administrative_assets_depreciation',
            'general_insurance',
            'audit_and_consulting_fees',
            'hospitality_and_transport'
        ]

class FinancialCostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialCosts
        fields = [
            'expense',
            'bank_interest_and_fees',
            'loan_late_penalties',
            'guarantee_fees',
            'discounting_expenses_on_receivables',
            'fund_transfer_and_bank_services'
        ]

class OtherOperatingCostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherOperatingCosts
        fields = [
            'expense',
            'bad_debts_and_written_off_expense',
            'fx_non_operating_gain_loss',
            'impairment_short_term_investments',
            'inventory_write_down',
            'asset_impairment',
            'impairment_long_term_investments',
            'fx_operating_gain_loss'
        ]

class ContingentAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContingentAccount
        fields = ['balance_sheet']

class ContingentAccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContingentAccounts
        fields = ['contingent_account', 'our_accounts_with_others', 'others_accounts_with_us']

class ContingentCounterpartiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContingentCounterparties
        fields = ['contingent_account', 'our_counterparties_with_others', 'others_counterparties_with_us', 'amount']

class CurrentAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentAsset
        fields = ['balance_sheet']

class CashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cash
        fields = [
            'current_asset',
            'cash_in_hand',
            'bank_balances',
            'petty_cash',
            'cash_in_transit'
        ]

class ShortTermInvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortTermInvestment
        fields = [
            'current_asset',
            'short_term_deposits',
            'tradable_stocks',
            'participation_bonds',
            'etf_investment_fund',
            'other_short_term_investments',
            'short_term_investment_impairment'
        ]

class TradeReceivableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeReceivable
        fields = [
            'current_asset',
            'trade_accounts_receivable',
            'trade_notes_receivable',
            'receivables_in_litigation',
            'notes_in_collection',
            'returned_cheques',
            'doubtful_receivables_provision'
        ]

class NonTradeReceivableSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonTradeReceivable
        fields = [
            'current_asset',
            'non_trade_accounts_receivable',
            'non_trade_notes_receivable',
            'employee_receivables',
            'director_receivables',
            'related_companies_receivables',
            'vat_receivable',
            'deposits_with_others',
            'dividends_receivable'
        ]

class ShareholderReceivableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareholderReceivable
        fields = ['current_asset', 'amount']

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = [
            'current_asset',
            'raw_materials',
            'work_in_progress',
            'finished_goods',
            'purchased_goods_for_sale',
            'spare_parts',
            'packaging_materials',
            'consignment_goods_with_others',
            'idle_items',
            'scrap_raw_materials',
            'inventory_impairment'
        ]

class OrdersAndPrepaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdersAndPrepayments
        fields = [
            'current_asset',
            'prepaid_goods_and_services',
            'prepaid_income_tax',
            'prepaid_rent',
            'prepaid_insurance',
            'orders_in_transit',
            'prepaid_loans',
            'prepaid_interest_on_loans',
            'other_prepayments'
        ]

class AssetsHeldForSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetsHeldForSale
        fields = ['current_asset', 'assets_held_for_sale', 'impairment_reserve']

class RevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Revenue
        fields = ['balance_sheet', 'total_amount']

class NetSalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetSales
        fields = ['revenue', 'amount']

class ServiceRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRevenue
        fields = ['revenue', 'amount']

class ForeignCurrencyRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForeignCurrencyRevenue
        fields = ['revenue', 'amount']

class OtherOperatingRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherOperatingRevenue
        fields = ['revenue', 'amount']