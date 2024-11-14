from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import DiagnosticAnalysisViewSet, chart_view


router = DefaultRouter()

router.register(r'', DiagnosticAnalysisViewSet,
                basename='diagnostic-analysis')

urlpatterns = router.urls

urlpatterns = [
    path('chart', chart_view, name='chart'),
]
