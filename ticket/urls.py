from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TicketViewSet
router = DefaultRouter()

router.register(r'tickets', TicketViewSet, basename='tickets')
urlpatterns = router.urls
