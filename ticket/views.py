from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from ticket.serializers import TicketSerializer
from .models import Ticket, Department, Agent


class TicketViewSet(viewsets.ModelViewSet):

    serializer_class = [TicketSerializer]
    queryset = Ticket.objects.all()

    def get_queryset(self):
        company = self.request.user.company
        return Ticket.objects.filter(issuer=company).all()
