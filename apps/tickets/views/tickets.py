from rest_framework.viewsets import ModelViewSet

from apps.tickets.views import ViewSetMixin
from apps.tickets.serializers import TicketListSerializer, TicketRetrieveSerializer
from apps.tickets.repositories import TicketRepository as _repo


class TicketViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {
        "list": TicketListSerializer,
        "retrieve": TicketRetrieveSerializer,
    }
    default_serializer_class = TicketListSerializer

    def get_queryset(self):
        company = self.get_company()
        return _repo.get_tickets_for_company(company)
