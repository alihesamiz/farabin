from django.urls import path


from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter


from apps.core.views import OTPViewSet

router = DefaultRouter()
router.register(r"", OTPViewSet, basename="otp")


urlpatterns = router.urls


urlpatterns += [
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
