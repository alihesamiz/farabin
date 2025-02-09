from django.urls import path

from rest_framework.routers import DefaultRouter

from finance.views import FinanceAnalysisViewSet, CompanyFinancialDataView


router = DefaultRouter()

router.register(r'', FinanceAnalysisViewSet,
                basename='finance-analysis')

urlpatterns = router.urls + [
    path('admin/finances/analysisreport/<uuid:company_id>/',
         CompanyFinancialDataView.as_view(), name='company_financial_data'),
]
