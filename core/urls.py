from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include
from .views import OTPViewSet

router = DefaultRouter()
router.register(r'', OTPViewSet, basename='otp')


urlpatterns = router.urls


urlpatterns += [
    # Use refresh token to get a new access token
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
