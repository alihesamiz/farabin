from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from ticket.serializers import TicketSerializer
from .models import Ticket, Department, Agent


class TicketViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = TicketSerializer

    def get_queryset(self):
        company = self.request.user.company
        return Ticket.objects.prefetch_related('answers').filter(issuer=company).all()

    def perform_create(self, serializer):
        # Assuming `company` is the related company of the current user
        company = self.request.user.company
        serializer.save(issuer=company)


    @action(detail=False,methods=['get','post','delete','put','patch'],url_path='comment',url_name='comments')
    def comments(self, request, pk=None):
        ticket = get_object_or_404(Ticket, pk=pk)
        if request.method == 'GET':
            serializer = TicketSerializer(ticket)
            return Response(serializer.data)
        elif request.method == 'POST':
            pass