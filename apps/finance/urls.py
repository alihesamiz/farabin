from django.urls import path

from rest_framework.routers import DefaultRouter

from apps.finance.views import (
    FinanceAnalysisViewSet,
    CompanyFinancialDataView,
    FinanceExcelViewSet,
    TaxDeclarationViewSet,
    BalanceReportViewSet,
)


router = DefaultRouter()

router.register(r"analysis", FinanceAnalysisViewSet, basename="finance-analysis")

router.register(r"tax-declarations", TaxDeclarationViewSet, basename="tax-declaration")

router.register(r"balance-reports", BalanceReportViewSet, basename="balance-report")

router.register(r"finance_excel", FinanceExcelViewSet, basename="finance-excel")


urlpatterns = router.urls + [
    path(
        "admin/finances/analysisreport/<uuid:company_id>/",
        CompanyFinancialDataView.as_view(),
        name="company_financial_data",
    ),
]
