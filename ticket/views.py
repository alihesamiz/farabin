from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

from ticket.serializers import TicketCommentCreateSerializer, TicketCommentSerializer, TicketSerializer
from .models import Ticket, Department, Agent, TicketAnswer


# class TicketViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]

#     serializer_class = TicketSerializer

#     def get_queryset(self):
#         company = self.request.user.company
#         return Ticket.objects.prefetch_related('answers').filter(issuer=company).all()

#     def perform_create(self, serializer):
#         # Assuming `company` is the related company of the current user
#         company = self.request.user.company
#         serializer.save(issuer=company)

#     @action(detail=False, methods=['get', 'post', 'delete', 'put', 'patch'], url_path='^(?P<pk>[^/.]+)/comment', url_name='comments')
#     def comments(self, request, pk=None):
#         ticket = get_object_or_404(Ticket, pk=pk)
#         print(ticket)
#         if request.method == 'GET':
#             print('lksjahdjklshad')
#             serializer = TicketSerializer(ticket)
#             return Response(serializer.data)
#         elif request.method == 'POST':
#             serializer = TicketCommentSerializer(ticket)
#             return Response(serializer.data)


class TicketViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TicketSerializer

    def get_queryset(self):
        company = self.request.user.company
        return Ticket.objects.prefetch_related('answers__comments').filter(issuer=company)

    def perform_create(self, serializer):
        company = self.request.user.company
        serializer.save(issuer=company)

    @action(detail=True, methods=['get', 'post'], url_path='comments', url_name='comments')
    def comments(self, request, pk=None):
        ticket = get_object_or_404(Ticket, pk=pk)

        if request.method == 'GET':
            serializer = TicketSerializer(ticket)
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
                print(answer.ticket)
                print(answer)
                serializer.save(answer=answer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
