from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import LogoutViewSet, OTPViewSet

router = DefaultRouter()
router.register(r'', OTPViewSet, basename='otp')
router.register(r'logout', LogoutViewSet, basename='logout')


urlpatterns = router.urls
