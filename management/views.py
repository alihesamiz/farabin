from django.db import IntegrityError

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from rest_framework import viewsets

from management.serializers import (HumanResourceSerializer, HumanResourceCreateSerializer, HumanResourceUpdateSerializer,
                                    PersonelInformationSerializer, PersonelInformationUpdateSerializer, PersonelInformationCreateSerializer, OrganizationChartFileSerializer)
from management.models import HumanResource, PersonelInformation, OrganizationChartBase
from management.paginations import PersonelPagination




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
    pagination_class = PersonelPagination

    def get_queryset(self):
        company = self.request.user.company
        
        human_resource_id = self.kwargs.get("human_resource_pk")

        if human_resource_id:
            return PersonelInformation.objects.select_related("human_resource").filter(
                human_resource__id=human_resource_id,
                human_resource__company=company
            )
        
        return PersonelInformation.objects.none()  
    
    def get_serializer_class(self):
        if self.action == "create":
            return PersonelInformationCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return PersonelInformationUpdateSerializer
        return PersonelInformationSerializer

    def perform_create(self, serializer):
        company = self.request.user.company
        
        human_resource_id = self.kwargs.get("human_resource_pk")  
        human_resource = company.hrfiles.filter(id=human_resource_id).first()

        if not human_resource:
            raise serializers.ValidationError(
                {"human_resource": "Invalid or missing HumanResource record for this company."}
            )

        serializer.save(human_resource=human_resource)



class OrganizationChartFileViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]

    serializer_class = OrganizationChartFileSerializer

    http_method_names = ['get']
    def get_queryset(self):
        company = self.request.user.company
        kind = company.tech_field
        return OrganizationChartBase.objects.filter(field=kind)
