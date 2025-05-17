from django.urls import path


from rest_framework.routers import DefaultRouter


from company.views import (
    CompanyProfileViewSet,
    DashboardViewSet,
    LifeCycleDeclineViewSet,
    LifeCycleFeatureViewSet,
    LifeCycleGrowthViewSet,
    LifeCycleIntroductionViewSet,
    LifeCycleMaturityViewSet,
    LifeCycleStateViewSet,
)


router = DefaultRouter()

router.register(r"profile", CompanyProfileViewSet, basename="profile")
router.register(r"features", LifeCycleFeatureViewSet, basename="lifecyclefeature")
router.register(r"declines", LifeCycleDeclineViewSet, basename="lifecycledecline")
router.register(r"maturities", LifeCycleMaturityViewSet, basename="lifecyclematurity")
router.register(r"growths", LifeCycleGrowthViewSet, basename="lifecyclegrowth")
router.register(
    r"introductions", LifeCycleIntroductionViewSet, basename="lifecycleintroduction"
)
router.register(r"places", LifeCycleStateViewSet, basename="lifecycleplace")
urlpatterns = router.urls

urlpatterns += [path("dashboard/", DashboardViewSet.as_view(), name="dashboard")]
