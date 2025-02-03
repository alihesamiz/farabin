from django.urls import path, include

from rest_framework.routers import DefaultRouter

from management.views import HumanResourceViewSet


router = DefaultRouter()

router.register(r'human-resource', HumanResourceViewSet, basename='tickets')


urlpatterns = router.urls
