from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import BalanceReportViewSet, CompanyProfileViewSet, DashboardViewSet, TaxDeclarationViewSet

router = DefaultRouter()

router.register(r'profile', CompanyProfileViewSet, basename='profile')

# router.register(r'dashboard', DashboardViewSet, basename='dashboard')

router.register(r'tax-declarations', TaxDeclarationViewSet,
                basename='tax-declaration')

router.register(r'balance-reports',
                BalanceReportViewSet, basename='balance-report')


urlpatterns = router.urls

urlpatterns += [path('dashboard/',
                     DashboardViewSet.as_view(), name='dashboard')]
