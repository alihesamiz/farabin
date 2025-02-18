from rest_framework.routers import DefaultRouter

from request.views import RequestViewSet

router = DefaultRouter()

router.register(r'requests', RequestViewSet,basename='requests')

urlpatterns = router.urls
