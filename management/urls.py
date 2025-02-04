from django.urls import path, include

from rest_framework.routers import DefaultRouter

from management.views import HumanResourceViewSet


router = DefaultRouter()

router.register(r'human-resource', HumanResourceViewSet, basename='human-resource')


urlpatterns = router.urls
