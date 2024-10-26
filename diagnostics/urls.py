from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import DiagnosticAnalysisView
router = DefaultRouter()
urlpatterns = router.urls
urlpatterns += [
    path('analysis/', DiagnosticAnalysisView.as_view(),
         name='diagnostic_analysis'),
]
