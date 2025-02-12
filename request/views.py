import importlib
import logging


from django.shortcuts import render
from django.conf import settings

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework import viewsets


from request.serializers import FinanceRequestSerializer,FinanceRequestSerializer
from request.models import FinanceRequest

# Create your views here.

logger = logging.getLogger("request")


class RequestViewSet(viewsets.ModelViewSet):
    REQUEST_TYPES = {
        app.lower(): getattr(importlib.import_module('request.serializers'), f"{app.title()}RequestSerializer")
        for app in settings.APP_REQUEST_TYPES
    }

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        company = self.request.user.company

        return FinanceRequest.objects.filter(company=company).order_by('-updated_at')

    def get_serializer_class(self):
        request_type = self.request.query_params.get('type')
        if request_type in self.REQUEST_TYPES:
            return self.REQUEST_TYPES[request_type]
        else:
            logger.warning(
                f"Invalid request type '{request_type}' requested by user {self.request.user.id}")
            raise NotFound("The requested type doesn't exist")
