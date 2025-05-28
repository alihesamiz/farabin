import importlib
import logging


from django.conf import settings

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework import viewsets


logger = logging.getLogger("request")


class RequestViewSet(viewsets.ModelViewSet):
    REQUEST_SERIALIZERS_TYPES = {
        app.lower(): getattr(
            importlib.import_module("apps.request.serializers"),
            f"{app.title()}RequestSerializer",
        )
        for app in settings.APP_REQUEST_TYPES
    }
    REQUEST_MODELS_TYPES = {
        app.lower(): getattr(
            importlib.import_module("apps.request.models"), f"{app.title()}Request"
        )
        for app in settings.APP_REQUEST_TYPES
    }

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        company = self.request.user.company
        request_type = self.request.query_params.get("type")

        logger.info(
            f"Fetching requests for company: {company.id}, user: {self.request.user.id}, type: {request_type}"
        )

        if request_type in self.REQUEST_MODELS_TYPES:
            logger.debug(f"Using model for request type: {request_type}")
            return (
                self.REQUEST_MODELS_TYPES[request_type]
                .objects.filter(company=company)
                .order_by("-updated_at")
            )
        else:
            logger.warning(
                f"Invalid request type '{request_type}' requested by user {self.request.user.id}"
            )
            raise NotFound("The requested type doesn't exist")

    def get_serializer_class(self):
        request_type = self.request.query_params.get("type")
        logger.info(
            f"Received request for type: {request_type} by user: {self.request.user.id}"
        )

        if request_type in self.REQUEST_SERIALIZERS_TYPES:
            logger.debug(f"Using serializer for request type: {request_type}")
            return self.REQUEST_SERIALIZERS_TYPES[request_type]
        else:
            logger.warning(
                f"Invalid request type '{request_type}' requested by user {self.request.user.id}"
            )
            raise NotFound("The requested type doesn't exist")
