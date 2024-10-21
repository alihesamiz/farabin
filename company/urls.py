from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import  CompanyProfileViewSet, DashboardViewSet

router = DefaultRouter()

router.register(r'profile', CompanyProfileViewSet, basename='profile')

router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = router.urls
