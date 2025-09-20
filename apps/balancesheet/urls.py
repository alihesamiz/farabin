# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.balancesheet.views import (
    BalanceSheetViewSet,
    BalanceSheetFileUploadViewSet,
    FixedAssetViewSet,
    IntangibleAssetViewSet,
    TangibleFixedAssetViewSet,
    AssetsInProgressViewSet,
    LongTermInvestmentViewSet,
    OtherNonCurrentAssetViewSet,
    CurrentLiabilityViewSet,
    TradeAccountsPayableViewSet,
    NonTradeAccountsPayableViewSet,
    ShareholderPayablesViewSet,
    DividendsPayableViewSet,
    ShortTermLoansViewSet,
    AdvancesAndDepositsViewSet,
    LiabilitiesRelatedToAssetsHeldForSaleViewSet,
    TaxProvisionViewSet,
    TaxPayableViewSet,
    LongTermLiabilityViewSet,
    LongTermAccountsPayableViewSet,
    LongTermLoansViewSet,
    LongTermProvisionsViewSet,
    EquityViewSet,
    InitialCapitalViewSet,
    CapitalIncreaseDecreaseViewSet,
    SharePremiumReserveViewSet,
    ShareDiscountReserveViewSet,
    LegalReserveViewSet,
    OtherReservesViewSet,
    RevaluationSurplusViewSet,
    ForeignCurrencyTranslationDifferenceViewSet,
    RetainedEarningsViewSet,
    ExpenseViewSet,
    ProductionCostsViewSet,
    DistributionAndMarketingCostsViewSet,
    GeneralAndAdministrativeCostsViewSet,
    FinancialCostsViewSet,
    OtherOperatingCostsViewSet,
    ContingentAccountViewSet,
    ContingentAccountsViewSet,
    ContingentCounterpartiesViewSet,
    CurrentAssetViewSet,
    CashViewSet,
    ShortTermInvestmentViewSet,
    TradeReceivableViewSet,
    NonTradeReceivableViewSet,
    ShareholderReceivableViewSet,
    InventoryViewSet,
    OrdersAndPrepaymentsViewSet,
    AssetsHeldForSaleViewSet,
    RevenueViewSet,
    NetSalesViewSet,
    ServiceRevenueViewSet,
    ForeignCurrencyRevenueViewSet,
    OtherOperatingRevenueViewSet,
)


# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'balancesheet-file-upload', BalanceSheetFileUploadViewSet, basename='balancesheet-file-upload')



    


# router.register(r'fixed-assets', FixedAssetViewSet)
# router.register(r'intangible-assets', IntangibleAssetViewSet)
# router.register(r'tangible-fixed-assets', TangibleFixedAssetViewSet)
# router.register(r'assets-in-progress', AssetsInProgressViewSet)
# router.register(r'long-term-investments', LongTermInvestmentViewSet)
# router.register(r'other-non-current-assets', OtherNonCurrentAssetViewSet)

# router.register(r'current-liabilities', CurrentLiabilityViewSet)
# router.register(r'trade-accounts-payable', TradeAccountsPayableViewSet)
# router.register(r'non-trade-accounts-payable', NonTradeAccountsPayableViewSet)
# router.register(r'shareholder-payables', ShareholderPayablesViewSet)
# router.register(r'dividends-payable', DividendsPayableViewSet)
# router.register(r'short-term-loans', ShortTermLoansViewSet)
# router.register(r'advances-and-deposits', AdvancesAndDepositsViewSet)
# router.register(r'liabilities-related-to-assets-held-for-sale', LiabilitiesRelatedToAssetsHeldForSaleViewSet)
# router.register(r'tax-provision', TaxProvisionViewSet)
# router.register(r'tax-payable', TaxPayableViewSet)

# router.register(r'long-term-liabilities', LongTermLiabilityViewSet)
# router.register(r'long-term-accounts-payable', LongTermAccountsPayableViewSet)
# router.register(r'long-term-loans', LongTermLoansViewSet)
# router.register(r'long-term-provisions', LongTermProvisionsViewSet)

# router.register(r'equities', EquityViewSet)
# router.register(r'initial-capital', InitialCapitalViewSet)
# router.register(r'capital-increase-decrease', CapitalIncreaseDecreaseViewSet)
# router.register(r'share-premium-reserve', SharePremiumReserveViewSet)
# router.register(r'share-discount-reserve', ShareDiscountReserveViewSet)
# router.register(r'legal-reserve', LegalReserveViewSet)
# router.register(r'other-reserves', OtherReservesViewSet)
# router.register(r'revaluation-surplus', RevaluationSurplusViewSet)
# router.register(r'foreign-currency-translation-difference', ForeignCurrencyTranslationDifferenceViewSet)
# router.register(r'retained-earnings', RetainedEarningsViewSet)

# router.register(r'expenses', ExpenseViewSet)
# router.register(r'production-costs', ProductionCostsViewSet)
# router.register(r'distribution-and-marketing-costs', DistributionAndMarketingCostsViewSet)
# router.register(r'general-and-administrative-costs', GeneralAndAdministrativeCostsViewSet)
# router.register(r'financial-costs', FinancialCostsViewSet)
# router.register(r'other-operating-costs', OtherOperatingCostsViewSet)

# router.register(r'contingent-account', ContingentAccountViewSet)
# router.register(r'contingent-accounts', ContingentAccountsViewSet)
# router.register(r'contingent-counterparties', ContingentCounterpartiesViewSet)

# router.register(r'current-assets', CurrentAssetViewSet)
# router.register(r'cash', CashViewSet)
# router.register(r'short-term-investment', ShortTermInvestmentViewSet)
# router.register(r'trade-receivable', TradeReceivableViewSet)
# router.register(r'non-trade-receivable', NonTradeReceivableViewSet)
# router.register(r'shareholder-receivable', ShareholderReceivableViewSet)
# router.register(r'inventory', InventoryViewSet)
# router.register(r'orders-and-prepayments', OrdersAndPrepaymentsViewSet)
# router.register(r'assets-held-for-sale', AssetsHeldForSaleViewSet)

# router.register(r'revenue', RevenueViewSet)
# router.register(r'net-sales', NetSalesViewSet)
# router.register(r'service-revenue', ServiceRevenueViewSet)
# router.register(r'foreign-currency-revenue', ForeignCurrencyRevenueViewSet)
# router.register(r'other-operating-revenue', OtherOperatingRevenueViewSet)




# Include router URLs
urlpatterns = [
    path('', include(router.urls)),
]
    