from django.db import IntegrityError

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from rest_framework import viewsets

from management.serializers import (HumanResourceSerializer, HumanResourceCreateSerializer, HumanResourceUpdateSerializer,
                                    PersonelInformationSerializer, PersonelInformationUpdateSerializer, PersonelInformationCreateSerializer, OrganizationChartFileSerializer)
from management.models import HumanResource, PersonelInformation, OrganizationChartBase

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
            raise ValidationError(
                {"error": "Each company can only have one Human Resource record."})


class PersonelInformationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        company = self.request.user.company
        return PersonelInformation.objects.select_related("human_resource").filter(human_resource__company=company)

    def get_serializer_class(self):
        if self.action == 'create':
            return PersonelInformationCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return PersonelInformationUpdateSerializer
        return PersonelInformationSerializer

    def perform_create(self, serializer):
        company = self.request.user.company
        human_resource = company.hrfiles.order_by(
            "-create_at").first()  # Ensure latest HR file is used
        if not human_resource:
            raise serializers.ValidationError(
                {"human_resource": "No HumanResource record found for this company."})
        serializer.save(human_resource=human_resource)


class OrganizationChartFileViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = OrganizationChartFileSerializer

    http_method_names = ['get']
    def get_queryset(self):
        company = self.request.user.company
        kind = company.tech_field
        return OrganizationChartBase.objects.filter(field=kind)
