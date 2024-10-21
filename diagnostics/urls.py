from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import LogoutViewSet, RegisterViewSet, OTPViewSet

router = DefaultRouter()
router.register(r'register', RegisterViewSet, basename='register')
router.register(r'otp', OTPViewSet, basename='otp')
router.register(r'logout', LogoutViewSet, basename='logout')
urlpatterns = router.urls
