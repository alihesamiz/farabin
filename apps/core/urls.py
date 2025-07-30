from rest_framework.routers import DefaultRouter  # type: ignore

from apps.core.views import (
    AuthViewSet,
    CityViewSet,
    ProvinceViewSet,
    UserProfileViewSet,
)

router = DefaultRouter()
router.register(r"", AuthViewSet, basename="auth")
router.register(r"profile", UserProfileViewSet, basename="profile")
router.register(r"city", CityViewSet, basename="city")
router.register(r"province", ProvinceViewSet, basename="province")


urlpatterns = router.urls
