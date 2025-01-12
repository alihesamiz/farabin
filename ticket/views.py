from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status

from .serializers import TicketChatSerializer, TicketCommentCreateSerializer, TicketCommentListSerializer, TicketCreateSerializer, TicketListSerializer, TicketDetailSerializer
from .paginations import TicketPagination
from .models import Ticket, TicketAnswer


# class TicketViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     pagination_class = TicketPagination

#     def get_queryset(self):
#         company = self.request.user.company
#         queryset = Ticket.objects.select_related('issuer').filter(issuer=company)#.prefetch_related('answers__comments')

#         service = self.request.query_params.get('service')
#         if service:
#             queryset = queryset.filter(service__name=service)
#         return queryset

#     def perform_create(self, serializer):
#         company = self.request.user.company
#         serializer.save(issuer=company)

#     def get_serializer_class(self):
#         # Select serializer based on the action type
#         if self.action == 'list':
#             return TicketListSerializer
#         elif self.action == 'retrieve':
#             return TicketDetailSerializer
#         elif self.action == 'create':
#             return TicketCreateSerializer
#         return TicketListSerializer

#     @action(detail=True, methods=['get', 'post'], url_path='comments', url_name='comments')
#     def comments(self, request, pk=None):
#         ticket = get_object_or_404(Ticket, pk=pk)

#         if request.method == 'GET':
#             comments_queryset = ticket.comments.all().order_by('-created_at')  # Assuming a related name 'comments'

#             # Apply pagination
#             page = self.paginate_queryset(comments_queryset)
#             if page is not None:
#                 serializer = TicketCommentListSerializer(page, many=True)  # Use a list serializer for comments
#                 return self.get_paginated_response(serializer.data)

#             serializer = TicketCommentListSerializer(comments_queryset, many=True)
#             return Response(serializer.data)

#         elif request.method == 'POST':
#             serializer = TicketCommentCreateSerializer(
#                 data=request.data,
#                 context={'ticket': ticket}
#             )
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class TicketViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     pagination_class = TicketPagination

#     def get_queryset(self):
#         company = self.request.user.company
#         queryset = Ticket.objects.select_related(
#             'issuer').filter(issuer=company)

#         service = self.request.query_params.get('service')
#         if service:
#             queryset = queryset.filter(service__name=service)
#         return queryset

#     def perform_create(self, serializer):
#         company = self.request.user.company
#         serializer.save(issuer=company)

#     def get_serializer_class(self):
#         if self.action == 'list':
#             return TicketListSerializer
#         elif self.action == 'retrieve':
#             return TicketDetailSerializer
#         elif self.action == 'create':
#             return TicketCreateSerializer
#         return TicketListSerializer

#     @action(detail=True, methods=['get', 'post'], url_path='comments', url_name='comments')
#     def comments(self, request, pk=None):
#         ticket = get_object_or_404(Ticket, pk=pk)

#         if request.method == 'GET':
#             serializer = TicketDetailSerializer(ticket)
#             return Response(serializer.data)

#         elif request.method == 'POST':
#             # Create a new comment for a specific TicketAnswer
#             # answer_id = request.data.get("answer_id")
#             # if not answer_id:
#             #     return Response({"error": "Answer ID is required"}, status=status.HTTP_400_BAD_REQUEST)

#             # answer = get_object_or_404(
#             #     TicketAnswer, pk=answer_id, ticket=ticket)
#             serializer = TicketCommentCreateSerializer(
#                 data=request.data,
#                 context={'ticket': ticket}  # , 'answer': answer}
#             )
#             if serializer.is_valid():
#                 serializer.save()  # answer=answer)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @action(detail=True, methods=['get'], url_path='chats', url_name='chats')
#     def chats(self, request, pk=None):
#         ticket = get_object_or_404(Ticket, pk=pk)

#         # Combine answers and comments
#         answers = ticket.answers.all()
#         comments = ticket.comments.all()
#         combined = sorted(
#             list(answers) + list(comments), key=lambda x: x.created_at, reverse=True
#         )

#         # Paginate the combined results
#         page = self.paginate_queryset(combined)
#         if page is not None:
#             serializer = TicketChatSerializer(page, many=True)
#             return self.get_paginated_response(serializer.data)

#         serializer = TicketChatSerializer(combined, many=True)
#         return Response(serializer.data)



class TicketViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = TicketPagination

    def get_queryset(self):
        company = self.request.user.company
        queryset = Ticket.objects.select_related(
            'issuer'
        ).filter(issuer=company)

        service = self.request.query_params.get('service')
        if service:
            queryset = queryset.filter(service__name=service)
        return queryset

    def perform_create(self, serializer):
        company = self.request.user.company
        serializer.save(issuer=company)

    def get_serializer_class(self):
        if self.action == 'list':
            return TicketListSerializer
        elif self.action == 'retrieve':
            return TicketDetailSerializer
        elif self.action == 'create':
            return TicketCreateSerializer
        return TicketListSerializer

    @action(detail=True, methods=['get', 'post'], url_path='comments', url_name='comments')
    def comments(self, request, pk=None):
        ticket = get_object_or_404(Ticket, pk=pk)

        if request.method == 'GET':
            comments = ticket.comments.all().order_by('-created_at')
            
            # Apply pagination
            page = self.paginate_queryset(comments)
            if page is not None:
                serializer = TicketChatSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = TicketChatSerializer(comments, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = TicketCommentCreateSerializer(
                data=request.data,
                context={'ticket': ticket}
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='chats', url_name='chats')
    def chats(self, request, pk=None):
        ticket = get_object_or_404(Ticket, pk=pk)

        # Combine answers and comments
        answers = ticket.answers.all()
        comments = ticket.comments.all()
        combined = sorted(
            list(answers) + list(comments), key=lambda x: x.created_at, reverse=True
        )

        # Apply pagination
        page = self.paginate_queryset(combined)
        if page is not None:
            serializer = TicketChatSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TicketChatSerializer(combined, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """
        Override list to add pagination to the main ticket list view.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Apply pagination
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to ensure ticket details are paginated when needed.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)