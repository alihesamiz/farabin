from rest_framework.routers import DefaultRouter

from apps.request.views import RequestViewSet

router = DefaultRouter()

router.register(r"", RequestViewSet, basename="requests")

urlpatterns = router.urls
