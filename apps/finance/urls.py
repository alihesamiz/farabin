from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.finance.views import (
    BalanceReportViewSet,
    CompanyFinancialDataView,
    # FinanceAnalysisViewSet,
    FinanceExcelViewSet,
    TaxDeclarationViewSet,
)
from apps.finance.views.financial import (
    FinanceAnalysisSummaryViewSet,
    FinancialChartViewSet,
    FinancialDataViewSet,
    TakenFileDateViewSet,
)

router = DefaultRouter()

# router.register(r"analysis", FinanceAnalysisViewSet, basename="finance-analysis")

router.register(r"tax-declarations", TaxDeclarationViewSet, basename="tax-declaration")
router.register(r"taken-years", TakenFileDateViewSet, basename="available-tax-years")

router.register(r"balance-reports", BalanceReportViewSet, basename="balance-report")

router.register(r"finance_excel", FinanceExcelViewSet, basename="finance-excel")

router.register(r"data", FinancialDataViewSet, basename="data")
router.register(r"chart", FinancialChartViewSet, basename="chart")
router.register(r"analysis", FinanceAnalysisSummaryViewSet, basename="analysis")


urlpatterns = router.urls + [
    path(
        "admin/finances/analysisreport/<uuid:company_id>/",
        CompanyFinancialDataView.as_view(),
        name="company_financial_data",
    ),
]
