from rest_framework.routers import DefaultRouter
from django.urls import path, include
# from .views import SoldProductFeeViewSet, ProfitLossStatementViewSet, BalanceReportViewSet, AccountTurnOverViewSet, FinancialAssetViewSet
from .views import FinancialDataView
router = DefaultRouter()
# router.register(r'sold-product-fees', SoldProductFeeViewSet, basename='sold-product-fees')
# router.register(r'profit-loss-statements', ProfitLossStatementViewSet, basename='profit-loss-statements')
# router.register(r'balance-reports', BalanceReportViewSet, basename='balance-reports')
# router.register(r'account-turnovers', AccountTurnOverViewSet, basename='account-turnovers')
# router.register(r'financial-assets', FinancialAssetViewSet, basename='financial-assets')

urlpatterns = router.urls
urlpatterns += path('financial-data/',
                    FinancialDataView.as_view(), name='financial-data'),
