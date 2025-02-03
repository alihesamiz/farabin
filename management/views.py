from django.db import IntegrityError

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets,status

from management.serializers import HumanResourceSerializer, HumanResourceCreateSerializer, HumanResourceUpdateSerializer
from management.models import HumanResource

# Create your views here.


class HumanResourceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        company = self.request.user.company
        return HumanResource.objects.filter(company=company)

    def get_serializer_class(self):
        if self.action == 'create':
            return HumanResourceCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return HumanResourceUpdateSerializer
        return HumanResourceSerializer
    
    def perform_create(self, serializer):
            try:
                serializer.save()
            except IntegrityError:
                raise ValidationError({"error": "Each company can only have one Human Resource record."})
