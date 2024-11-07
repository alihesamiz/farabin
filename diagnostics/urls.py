from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import DiagnosticAnalysisViewSet


router = DefaultRouter()

router.register(r'', DiagnosticAnalysisViewSet,
                basename='diagnostic-analysis')

# router.register(r'anal', AnalysisReportViewSet, basename='analysis-report')
urlpatterns = router.urls
