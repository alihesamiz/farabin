from rest_framework.routers import DefaultRouter

from ticket.views import TicketViewSet


router = DefaultRouter()

router.register(r'', TicketViewSet, basename='tickets')
urlpatterns = router.urls