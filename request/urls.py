from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import RequestViewSet

router = DefaultRouter()

router.register(r'requests', RequestViewSet,basename='requests')

urlpatterns = router.urls
