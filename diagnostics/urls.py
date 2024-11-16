from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import DiagnosticAnalysisViewSet, CompanyFinancialDataView


router = DefaultRouter()

router.register(r'', DiagnosticAnalysisViewSet,
                basename='diagnostic-analysis')

urlpatterns = router.urls + [
    path('company-financial-data/<uuid:company_id>/',
         CompanyFinancialDataView.as_view(), name='company_financial_data'),
]
