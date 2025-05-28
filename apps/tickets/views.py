import logging


from django.shortcuts import get_object_or_404


from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, status


from apps.tickets.serializers import (
    TicketChatSerializer,
    TicketCommentCreateSerializer,
    TicketCreateSerializer,
    TicketListSerializer,
    TicketDetailSerializer,
)
from apps.tickets.paginations import TicketPagination
from apps.tickets.models import Ticket


logger = logging.getLogger("tickets")


class TicketViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = TicketPagination

    def get_queryset(self):
        company = self.request.user.company
        logger.info(
            f"Fetching tickets for company: {company.id}, user: {self.request.user.id}"
        )

        queryset = Ticket.objects.select_related("issuer").filter(issuer=company)

        service = self.request.query_params.get("service")
        if service:
            queryset = queryset.filter(service__name=service)
            logger.debug(f"Filtered tickets by service: {service}")

        return queryset

    def perform_create(self, serializer):
        company = self.request.user.company
        logger.info(
            f"Creating a new ticket for company: {company.id}, user: {self.request.user.id}"
        )
        serializer.save(issuer=company)

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        elif self.action == "retrieve":
            return TicketDetailSerializer
        elif self.action == "create":
            return TicketCreateSerializer
        return TicketListSerializer

    @action(
        detail=True, methods=["get", "post"], url_path="comments", url_name="comments"
    )
    def comments(self, request, pk=None):
        logger.info(
            f"Handling comments for ticket ID: {pk}, user: {self.request.user.id}"
        )

        ticket = get_object_or_404(Ticket, pk=pk)

        if request.method == "GET":
            comments = ticket.comments.all().order_by("-created_at")
            logger.debug(f"Retrieved {comments.count()} comments for ticket ID: {pk}")

            page = self.paginate_queryset(comments)
            if page is not None:
                serializer = TicketChatSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = TicketChatSerializer(comments, many=True)
            return Response(serializer.data)

        elif request.method == "POST":
            serializer = TicketCommentCreateSerializer(
                data=request.data, context={"ticket": ticket}
            )
            if serializer.is_valid():
                serializer.save()
                logger.info(
                    f"Comment added successfully for ticket ID: {pk}, user: {self.request.user.id}"
                )
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            logger.warning(
                f"Failed to create comment for ticket ID: {pk}, user: {self.request.user.id}. Errors: {serializer.errors}"
            )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"], url_path="chats", url_name="chats")
    def chats(self, request, pk=None):
        logger.info(
            f"Fetching chat history for ticket ID: {pk}, user: {self.request.user.id}"
        )

        ticket = get_object_or_404(Ticket, pk=pk)

        answers = ticket.answers.all()
        comments = ticket.comments.all()
        combined = sorted(
            list(answers) + list(comments), key=lambda x: x.created_at, reverse=True
        )

        logger.debug(f"Fetched {len(combined)} chat messages for ticket ID: {pk}")

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

        logger.info(f"Listing tickets for user: {self.request.user.id}")

        queryset = self.filter_queryset(self.get_queryset())

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
        logger.info(
            f"Retrieving ticket ID: {instance.id}, user: {self.request.user.id}"
        )

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
