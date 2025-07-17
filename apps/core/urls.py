from django.urls import path  # type: ignore


from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter  # type: ignore


from apps.core.views import AuthViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r"", AuthViewSet, basename="auth")
router.register(r"profile", UserProfileViewSet, basename="profile")


urlpatterns = router.urls


urlpatterns += [
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
