from rest_framework.routers import DefaultRouter

from packages.views import OrderViewSet, PackageViewSet, ServiceViewSet, SubscriptionsViewSet

router = DefaultRouter()
router.register(r"list", PackageViewSet, basename="packages")
router.register(r"services", ServiceViewSet, basename="services")
router.register(r"subscription", SubscriptionsViewSet,
                basename="subscriptions")
router.register(r"order", OrderViewSet, basename="orders")


urlpatterns = router.urls
