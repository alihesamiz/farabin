from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Ticket, Department, Agent
from .serializers import TicketSerializer
# Create your views here.

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter tickets by user or agent, depending on who is requesting
        if self.request.user.is_staff:
            return Ticket.objects.filter(agent__user=self.request.user)
        return Ticket.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        department_id = serializer.validated_data['department'].id
        department = get_object_or_404(Department, id=department_id)

        # Assign priority based on user type (VIP users get high priority automatically)
        priority = serializer.validated_data.get('priority')


        serializer.save(user=user, priority=priority, department=department)

    def update(self, request, *args, **kwargs):
        # Handle PUT/PATCH for updating ticket status, agent assignments, etc.
        ticket = self.get_object()
        serializer = self.get_serializer(ticket, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)