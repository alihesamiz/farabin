from django.shortcuts import render

from apps.balancesheet.serializers import (

    BalanceSheetFileUploadSerializer,


    BalanceSheetSerializer,
    FixedAssetSerializer,
    IntangibleAssetSerializer,
    TangibleFixedAssetSerializer,
    AssetsInProgressSerializer,
    LongTermInvestmentSerializer,
    OtherNonCurrentAssetSerializer,
    CurrentLiabilitySerializer,
    TradeAccountsPayableSerializer,
    NonTradeAccountsPayableSerializer,
    ShareholderPayablesSerializer,
    DividendsPayableSerializer,
    ShortTermLoansSerializer,
    AdvancesAndDepositsSerializer,
    LiabilitiesRelatedToAssetsHeldForSaleSerializer,
    TaxProvisionSerializer,
    TaxPayableSerializer,
    LongTermLiabilitySerializer,
    LongTermAccountsPayableSerializer,
    LongTermLoansSerializer,
    LongTermProvisionsSerializer,
    EquitySerializer,
    InitialCapitalSerializer,
    CapitalIncreaseDecreaseSerializer,
    SharePremiumReserveSerializer,
    ShareDiscountReserveSerializer,
    LegalReserveSerializer,
    OtherReservesSerializer,
    RevaluationSurplusSerializer,
    ForeignCurrencyTranslationDifferenceSerializer,
    RetainedEarningsSerializer,
    ExpenseSerializer,
    ProductionCostsSerializer,
    DistributionAndMarketingCostsSerializer,
    GeneralAndAdministrativeCostsSerializer,
    FinancialCostsSerializer,
    OtherOperatingCostsSerializer,
    ContingentAccountSerializer,
    ContingentAccountsSerializer,
    ContingentCounterpartiesSerializer,
    CurrentAssetSerializer,
    CashSerializer,
    ShortTermInvestmentSerializer,
    TradeReceivableSerializer,
    NonTradeReceivableSerializer,
    ShareholderReceivableSerializer,
    InventorySerializer,
    OrdersAndPrepaymentsSerializer,
    AssetsHeldForSaleSerializer,
    RevenueSerializer,
    NetSalesSerializer,
    ServiceRevenueSerializer,
    ForeignCurrencyRevenueSerializer,
    OtherOperatingRevenueSerializer,
)

############### Models

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




from rest_framework import viewsets




# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings
import os

from .tasks import analyze_balance_sheet

import os
from datetime import datetime
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import BalanceSheetFileUploadSerializer
from .tasks import analyze_balance_sheet
from apps.company.models.company import CompanyUser


import logging
logger = logging.getLogger(__name__)





class BalanceSheetFileUploadViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for uploading a file and passing it to Celery
    """


    @action(detail=False, methods=['post'])
    def upload(self, request):
        serializer = BalanceSheetFileUploadSerializer(data=request.data)
        if serializer.is_valid():
            
            file_obj = serializer.validated_data['file']
            try : 
                company_id = CompanyUser.objects.get(user=request.user).company.id
                company_name = CompanyUser.objects.get(user=request.user).company.title
               
            except :
                return Response({
                    "errors": "User is not associated with any company.",
                }, status=status.HTTP_400_BAD_REQUEST)
          


            today_date = datetime.now().strftime('%Y-%m-%d')  # Format: YYYY-MM-DD

            # Construct the dynamic folder path
            folder_path = os.path.join('balance_sheet', f"{company_name}_{today_date}")
            full_folder_path = os.path.join(settings.MEDIA_ROOT, folder_path)
            
            # Ensure the directory exists
            os.makedirs(full_folder_path, exist_ok=True)

            # Construct the full file path
            file_path = os.path.join(full_folder_path, file_obj.name)

            # Save file to the constructed path
            with open(file_path, 'wb+') as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)

            # Call Celery task
            #analyze_balance_sheet.delay(file_path)
            response = analyze_balance_sheet(file_path, company_id=company_id, year=1404)  # Synchronous call for now
            #

            return Response({
                "message": f"File uploaded successfully. -> {response}",
                "file_path": file_path,
                "company": company_name,
                "date": today_date
            }, status=status.HTTP_201_CREATED)


        return Response({
            "errors": serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)













# NOT NEEDED NOW

class BalanceSheetViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing balance sheet instances.
    """
    queryset = BalanceSheet.objects.all()      
    serializer_class = BalanceSheetSerializer


class FixedAssetViewSet(viewsets.ModelViewSet):
    queryset = FixedAsset.objects.all()
    serializer_class = FixedAssetSerializer


class IntangibleAssetViewSet(viewsets.ModelViewSet):
    queryset = IntangibleAsset.objects.all()
    serializer_class = IntangibleAssetSerializer


class TangibleFixedAssetViewSet(viewsets.ModelViewSet):
    queryset = TangibleFixedAsset.objects.all()
    serializer_class = TangibleFixedAssetSerializer


class AssetsInProgressViewSet(viewsets.ModelViewSet):
    queryset = AssetsInProgress.objects.all()
    serializer_class = AssetsInProgressSerializer


class LongTermInvestmentViewSet(viewsets.ModelViewSet):
    queryset = LongTermInvestment.objects.all()
    serializer_class = LongTermInvestmentSerializer


class OtherNonCurrentAssetViewSet(viewsets.ModelViewSet):
    queryset = OtherNonCurrentAsset.objects.all()
    serializer_class = OtherNonCurrentAssetSerializer


class CurrentLiabilityViewSet(viewsets.ModelViewSet):
    queryset = CurrentLiability.objects.all()
    serializer_class = CurrentLiabilitySerializer


class TradeAccountsPayableViewSet(viewsets.ModelViewSet):
    queryset = TradeAccountsPayable.objects.all()
    serializer_class = TradeAccountsPayableSerializer

class NonTradeAccountsPayableViewSet(viewsets.ModelViewSet):
    queryset = NonTradeAccountsPayable.objects.all()
    serializer_class = NonTradeAccountsPayableSerializer

class ShareholderPayablesViewSet(viewsets.ModelViewSet):
    queryset = ShareholderPayables.objects.all()
    serializer_class = ShareholderPayablesSerializer

class DividendsPayableViewSet(viewsets.ModelViewSet):
    queryset = DividendsPayable.objects.all()
    serializer_class = DividendsPayableSerializer

class ShortTermLoansViewSet(viewsets.ModelViewSet):
    queryset = ShortTermLoans.objects.all()
    serializer_class = ShortTermLoansSerializer

class AdvancesAndDepositsViewSet(viewsets.ModelViewSet):
    queryset = AdvancesAndDeposits.objects.all()
    serializer_class = AdvancesAndDepositsSerializer

class LiabilitiesRelatedToAssetsHeldForSaleViewSet(viewsets.ModelViewSet):
    queryset = LiabilitiesRelatedToAssetsHeldForSale.objects.all()
    serializer_class = LiabilitiesRelatedToAssetsHeldForSaleSerializer

class TaxProvisionViewSet(viewsets.ModelViewSet):
    queryset = TaxProvision.objects.all()
    serializer_class = TaxProvisionSerializer

class TaxPayableViewSet(viewsets.ModelViewSet):
    queryset = TaxPayable.objects.all()
    serializer_class = TaxPayableSerializer

class LongTermLiabilityViewSet(viewsets.ModelViewSet):
    queryset = LongTermLiability.objects.all()
    serializer_class = LongTermLiabilitySerializer

class LongTermAccountsPayableViewSet(viewsets.ModelViewSet):
    queryset = LongTermAccountsPayable.objects.all()
    serializer_class = LongTermAccountsPayableSerializer

class LongTermLoansViewSet(viewsets.ModelViewSet):
    queryset = LongTermLoans.objects.all()
    serializer_class = LongTermLoansSerializer

class LongTermProvisionsViewSet(viewsets.ModelViewSet):
    queryset = LongTermProvisions.objects.all()
    serializer_class = LongTermProvisionsSerializer

class EquityViewSet(viewsets.ModelViewSet):
    queryset = Equity.objects.all()
    serializer_class = EquitySerializer

class InitialCapitalViewSet(viewsets.ModelViewSet):
    queryset = InitialCapital.objects.all()
    serializer_class = InitialCapitalSerializer

class CapitalIncreaseDecreaseViewSet(viewsets.ModelViewSet):
    queryset = CapitalIncreaseDecrease.objects.all()
    serializer_class = CapitalIncreaseDecreaseSerializer

class SharePremiumReserveViewSet(viewsets.ModelViewSet):
    queryset = SharePremiumReserve.objects.all()
    serializer_class = SharePremiumReserveSerializer

class ShareDiscountReserveViewSet(viewsets.ModelViewSet):
    queryset = ShareDiscountReserve.objects.all()
    serializer_class = ShareDiscountReserveSerializer

class LegalReserveViewSet(viewsets.ModelViewSet):
    queryset = LegalReserve.objects.all()
    serializer_class = LegalReserveSerializer

class OtherReservesViewSet(viewsets.ModelViewSet):
    queryset = OtherReserves.objects.all()
    serializer_class = OtherReservesSerializer

class RevaluationSurplusViewSet(viewsets.ModelViewSet):
    queryset = RevaluationSurplus.objects.all()
    serializer_class = RevaluationSurplusSerializer

class ForeignCurrencyTranslationDifferenceViewSet(viewsets.ModelViewSet):
    queryset = ForeignCurrencyTranslationDifference.objects.all()
    serializer_class = ForeignCurrencyTranslationDifferenceSerializer

class RetainedEarningsViewSet(viewsets.ModelViewSet):
    queryset = RetainedEarnings.objects.all()
    serializer_class = RetainedEarningsSerializer

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class ProductionCostsViewSet(viewsets.ModelViewSet):
    queryset = ProductionCosts.objects.all()
    serializer_class = ProductionCostsSerializer

class DistributionAndMarketingCostsViewSet(viewsets.ModelViewSet):
    queryset = DistributionAndMarketingCosts.objects.all()
    serializer_class = DistributionAndMarketingCostsSerializer

class GeneralAndAdministrativeCostsViewSet(viewsets.ModelViewSet):
    queryset = GeneralAndAdministrativeCosts.objects.all()
    serializer_class = GeneralAndAdministrativeCostsSerializer

class FinancialCostsViewSet(viewsets.ModelViewSet):
    queryset = FinancialCosts.objects.all()
    serializer_class = FinancialCostsSerializer

class OtherOperatingCostsViewSet(viewsets.ModelViewSet):
    queryset = OtherOperatingCosts.objects.all()
    serializer_class = OtherOperatingCostsSerializer

class ContingentAccountViewSet(viewsets.ModelViewSet):
    queryset = ContingentAccount.objects.all()
    serializer_class = ContingentAccountSerializer

class ContingentAccountsViewSet(viewsets.ModelViewSet):
    queryset = ContingentAccounts.objects.all()
    serializer_class = ContingentAccountsSerializer

class ContingentCounterpartiesViewSet(viewsets.ModelViewSet):
    queryset = ContingentCounterparties.objects.all()
    serializer_class = ContingentCounterpartiesSerializer

class CurrentAssetViewSet(viewsets.ModelViewSet):
    queryset = CurrentAsset.objects.all()
    serializer_class = CurrentAssetSerializer

class CashViewSet(viewsets.ModelViewSet):
    queryset = Cash.objects.all()
    serializer_class = CashSerializer

class ShortTermInvestmentViewSet(viewsets.ModelViewSet):
    queryset = ShortTermInvestment.objects.all()
    serializer_class = ShortTermInvestmentSerializer

class TradeReceivableViewSet(viewsets.ModelViewSet):
    queryset = TradeReceivable.objects.all()
    serializer_class = TradeReceivableSerializer

class NonTradeReceivableViewSet(viewsets.ModelViewSet):
    queryset = NonTradeReceivable.objects.all()
    serializer_class = NonTradeReceivableSerializer

class ShareholderReceivableViewSet(viewsets.ModelViewSet):
    queryset = ShareholderReceivable.objects.all()
    serializer_class = ShareholderReceivableSerializer

class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

class OrdersAndPrepaymentsViewSet(viewsets.ModelViewSet):
    queryset = OrdersAndPrepayments.objects.all()
    serializer_class = OrdersAndPrepaymentsSerializer

class AssetsHeldForSaleViewSet(viewsets.ModelViewSet):
    queryset = AssetsHeldForSale.objects.all()
    serializer_class = AssetsHeldForSaleSerializer

class RevenueViewSet(viewsets.ModelViewSet):
    queryset = Revenue.objects.all()
    serializer_class = RevenueSerializer

class NetSalesViewSet(viewsets.ModelViewSet):
    queryset = NetSales.objects.all()
    serializer_class = NetSalesSerializer

class ServiceRevenueViewSet(viewsets.ModelViewSet):
    queryset = ServiceRevenue.objects.all()
    serializer_class = ServiceRevenueSerializer

class ForeignCurrencyRevenueViewSet(viewsets.ModelViewSet):
    queryset = ForeignCurrencyRevenue.objects.all()
    serializer_class = ForeignCurrencyRevenueSerializer

class OtherOperatingRevenueViewSet(viewsets.ModelViewSet):
    queryset = OtherOperatingRevenue.objects.all()
    serializer_class = OtherOperatingRevenueSerializer