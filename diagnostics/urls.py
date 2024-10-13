from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import LogoutViewSet, RegisterViewSet, OTPViewSet, CompanyProfileViewSet, DashboardViewSet

router = DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'otp', OTPViewSet, basename='otp')
router.register(r'profile', CompanyProfileViewSet, basename='profile')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')
router.register(r'logout', LogoutViewSet, basename='logout')
urlpatterns = router.urls
