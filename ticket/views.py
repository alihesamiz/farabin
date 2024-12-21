from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from .serializers import TicketCommentCreateSerializer, TicketCommentSerializer, TicketListSerializer, TicketDetailSerializer
from .models import Ticket, Department, Agent, TicketAnswer
from .paginations import TicketPagination

class TicketViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = TicketPagination

    def get_queryset(self):
        company = self.request.user.company
        return Ticket.objects.select_related('issuer').prefetch_related('answers__comments').filter(issuer=company)

    def perform_create(self, serializer):
        company = self.request.user.company
        serializer.save(issuer=company)
        
    def get_serializer_class(self):
        # Select serializer based on the action type
        if self.action == 'list':
            return TicketListSerializer
        elif self.action == 'retrieve':
            return TicketDetailSerializer
        return TicketListSerializer

    @action(detail=True, methods=['get', 'post'], url_path='comments', url_name='comments')
    def comments(self, request, pk=None):
        ticket = get_object_or_404(Ticket, pk=pk)

        if request.method == 'GET':
            serializer = TicketDetailSerializer(ticket)
            return Response(serializer.data)

        elif request.method == 'POST':
            # Create a new comment for a specific TicketAnswer
            answer_id = request.data.get("answer_id")
            if not answer_id:
                return Response({"error": "Answer ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            answer = get_object_or_404(TicketAnswer, pk=answer_id, ticket=ticket)
            serializer = TicketCommentCreateSerializer(
                data=request.data,
                context={'ticket': ticket, 'answer': answer}
            )
            if serializer.is_valid():
                serializer.save(answer=answer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
