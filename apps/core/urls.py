from rest_framework.routers import DefaultRouter  # type: ignore
from django.urls import path
from apps.core.views import (
    AuthViewSet,
    CityViewSet,
    ProvinceViewSet,
    UserProfileViewSet,
    CustomTokenObtainPairView,
    LogoutView,
    CustomTokenRefreshView,
    ProtectedView
)

router = DefaultRouter()
router.register(r"", AuthViewSet, basename="auth")
router.register(r"profile", UserProfileViewSet, basename="profile")
router.register(r"city", CityViewSet, basename="city")
router.register(r"province", ProvinceViewSet, basename="province")

patterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    # Add more API endpoints as needed
]



urlpatterns = router.urls + patterns
