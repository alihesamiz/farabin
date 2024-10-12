from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RegisterViewSet, OTPViewSet, CompanyProfileViewSet

router = DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'otp', OTPViewSet, basename='otp')
router.register(r'profile', CompanyProfileViewSet, basename='profile')

urlpatterns = [
    # Include the router urls
    path('api/', include(router.urls)),
]
