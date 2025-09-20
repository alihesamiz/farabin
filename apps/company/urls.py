from rest_framework.routers import DefaultRouter

from apps.company.views import (
    CompanyProfileViewSet,
    CompanyUserViewSet,
    LifeCycleDeclineViewSet,
    LifeCycleFeatureViewSet,
    LifeCycleGrowthViewSet,
    LifeCycleIntroductionViewSet,
    LifeCycleMaturityViewSet,
    LifeCycleStateViewSet, 
)

router = DefaultRouter()

router.register(r"profile", CompanyProfileViewSet, basename="profile")
router.register(r"users", CompanyUserViewSet, basename="users")
router.register(r"features", LifeCycleFeatureViewSet, basename="lifecyclefeature")
router.register(r"declines", LifeCycleDeclineViewSet, basename="lifecycledecline")
router.register(r"maturities", LifeCycleMaturityViewSet, basename="lifecyclematurity")
router.register(r"growths", LifeCycleGrowthViewSet, basename="lifecyclegrowth")
router.register(
    r"introductions", LifeCycleIntroductionViewSet, basename="lifecycleintroduction"
)
router.register(r"places", LifeCycleStateViewSet, basename="lifecycleplace")
urlpatterns = router.urls
