from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BalanceReportViewSet, CompanyProfileViewSet, DashboardViewSet, TaxDeclarationViewSet

router = DefaultRouter()

router.register(r'profile', CompanyProfileViewSet, basename='profile')

router.register(r'dashboard', DashboardViewSet, basename='dashboard')

router.register(r'tax-declarations', TaxDeclarationViewSet,
                basename='taxdeclaration')

router.register(r'balance-reports', BalanceReportViewSet)


urlpatterns = router.urls
