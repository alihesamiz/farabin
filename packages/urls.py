from rest_framework_nested.routers import NestedDefaultRouter
from rest_framework.routers import DefaultRouter

from packages.views import PackageViewSet, ServiceViewSet

router = DefaultRouter()
router.register(r"", PackageViewSet, basename="packages")
router.register(r"services", ServiceViewSet, basename="services")


urlpatterns = router.urls
