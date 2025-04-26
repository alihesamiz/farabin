import logging
import os


from django.utils.translation import gettext_lazy as _
from django.http import FileResponse
from django.db import IntegrityError


from rest_framework import (serializers, viewsets, status)
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response


from management.serializers import (ChartNodeSerializer, HumanResourceSerializer, HumanResourceCreateSerializer, HumanResourceUpdateSerializer,
                                    PersonelInformationSerializer, PersonelInformationUpdateSerializer, PersonelInformationCreateSerializer,
                                    OrganizationChartFileSerializer, SWOTMatrixCreateSerializer, SWOTStrengthOptionSerializer, SWOTWeaknessOptionSerializer, SWOTOpportunityOptionSerializer, SWOTThreatOptionSerializer, SWOTMatrixSerializer)

from management.models import HumanResource, PersonelInformation, OrganizationChartBase, SWOTMatrix, SWOTOpportunityOption, SWOTStrengthOption, SWOTThreatOption, SWOTWeaknessOption
from management.paginations import PersonelPagination
from management.utils import get_file_field

logger = logging.getLogger("management")


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
            logger.info("Attempting to save new Human Resource record.")
            serializer.save()
            logger.info("Human Resource record created successfully.")
        except IntegrityError:
            logger.error(
                "IntegrityError: Trying to create a second Human Resource record for the company.")
            raise ValidationError(
                {"error": _("Each company can only have one Human Resource record. To replace, you must first delete the previous record.")})
        except Exception as e:
            logger.error(
                f"Error while saving new Human Resource record: {str(e)}")
            raise ValidationError(
                {"error": _("An error occurred while saving the Human Resource record.")})


class PersonelInformationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = PersonelPagination

    def get_queryset(self):
        company = self.request.user.company

        human_resource_id = self.kwargs.get("human_resource_pk")

        if human_resource_id:
            logger.info(
                f"Fetching PersonelInformation for HumanResource ID: {human_resource_id}")
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
            logger.error(
                f"HumanResource ID {human_resource_id} not found for company {company.company_title}.")
            raise serializers.ValidationError(
                {"human_resource": _(
                    "Invalid or missing HumanResource record for this company.")}
            )

        logger.info(
            f"Creating PersonelInformation for HumanResource ID: {human_resource_id}")
        serializer.save(human_resource=human_resource)


class OrganizationChartFileViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationChartFileSerializer
    http_method_names = ['get']

    def get_queryset(self):
        field = self.request.user.company.tech_field
        file_field = get_file_field(field)
        return OrganizationChartBase.objects.filter(field=file_field)

    @action(detail=False, methods=['GET'], url_name='download', url_path='download')
    def download(self, request):

        queryset = self.get_queryset().first()
        if not queryset:
            logger.warning(
                "No associated OrganizationChart file found for the user's profile.")
            return Response({"error": _("Not found an associated file with your profile")}, status=status.HTTP_404_NOT_FOUND)

        file_path = queryset.position_excel.path
        company_name = request.user.company.company_title
        logger.info(
            f"Returning Excel file for company {company_name}. File path: {file_path}")

        return FileResponse(open(file_path, "rb"), as_attachment=True, filename=os.path.basename(file_path))


class ChartNodeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ChartNodeSerializer

    def get_queryset(self):
        company = self.request.user.company
        return PersonelInformation.objects.filter(human_resource__company=company)

    def list(self, request, *args, **kwargs):
        """
        Default list method that returns grouped data with aggregated reports-to positions.
        """
        queryset = self.get_queryset()
        grouped_data = {}
        for person in queryset:
            pos = person.position

            if pos not in grouped_data:
                grouped_data[pos] = {
                    'personnel': [],
                    'aggregated_reports_to': set(),
                    'aggregated_cooperates_with': set()
                }
            grouped_data[pos]['personnel'].append(person.position)

            if person.reports_to.exists():
                [
                    grouped_data[pos]['aggregated_reports_to'].add(
                        report.position) for report in person.reports_to.all(
                    )
                ]

            if person.cooperates_with.exists():
                [
                    grouped_data[pos]['aggregated_cooperates_with'].add(
                        cooperate.position) for cooperate in person.cooperates_with.all()
                ]

        response_data = {}
        for pos, data in grouped_data.items():
            response_data[pos] = {
                'aggregated_reports_to': list(data['aggregated_reports_to']),
                'aggregated_cooperates_with': list(data['aggregated_cooperates_with'])
            }

        return Response(response_data)

    @action(detail=False, methods=['get'], url_name='positions', url_path='positions')
    def by_positions(self, request, *args, **kwargs):
        """
        Custom action that expects a query parameter 'positions' (comma-separated values).
        It returns a JSON response where each key is a position and the value is a list
        of personnel (serialized) who hold that position.

        Example request:
            GET /chartnodes/positions/?pos=Manager,Developer
        """
        positions_param = request.query_params.get('pos')
        if not positions_param:
            return Response(
                {"detail": "Query parameter 'positions' is required."},
                status=400
            )

        positions = [pos.strip() for pos in positions_param.split(',')]

        queryset = self.get_queryset().filter(position__in=positions)

        grouped_personnel = {}
        for person in queryset:
            pos = person.position

            if pos not in grouped_personnel:
                grouped_personnel[pos] = []

            serialized_person = self.get_serializer(person).data
            grouped_personnel[pos].append(serialized_person)

        return Response(grouped_personnel)


class SWOTStrengthOptionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SWOTStrengthOptionSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        company = self.request.user.company
        return SWOTStrengthOption.objects.prefetch_related("swot_matrices_strengths").filter(
            swot_matrices_strengths__company=company
        ).distinct()


class SWOTWeaknessOptionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SWOTWeaknessOptionSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        company = self.request.user.company
        return SWOTWeaknessOption.objects.filter(
            swot_matrices_weaknesses__company=company
        ).distinct()


class SWOTOppotunityOptionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SWOTOpportunityOptionSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        company = self.request.user.company
        return SWOTOpportunityOption.objects.filter(
            swot_matrices_opportunities__company=company
        ).distinct()


class SWOTThreatOptionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SWOTThreatOptionSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        company = self.request.user.company
        return SWOTThreatOption.objects.filter(
            swot_matrices_threats__company=company
        ).distinct()


class SWOTMatrixViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SWOTMatrixSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == "create":
            return SWOTMatrixCreateSerializer
        return SWOTMatrixSerializer

    def get_queryset(self):
        company = self.request.user.company
        return SWOTMatrix.objects.prefetch_related("company").filter(company=company)

    # @action(detail=True, methods=['get'])
    # def strength(self, request, **kwargs):
    #     company = self.request.user.company
    #     strengths = SWOTMatrix.objects.get(company=company).strengths.all()
    #     data = SWOTStrengthOptionSerializer(strengths, many=True).data
    #     return Response(data)

    # @action(detail=True, methods=['get'])
    # def weakness(self, request, **kwargs):
    #     company = self.request.user.company
    #     weaknesses = SWOTWeaknessOption.objects.filter(company=company)
    #     data = SWOTWeaknessOptionSerializer(weaknesses, many=True).data
    #     return Response(data)

    # @action(detail=True, methods=['get'])
    # def opportunity(self, request, **kwargs):
    #     company = self.request.user.company
    #     opportunities = SWOTOpportunityOption.objects.filter(company=company)
    #     data = SWOTOpportunityOptionSerializer(opportunities, many=True).data
    #     return Response(data)

    # @action(detail=True, methods=['get'])
    # def threat(self, request, **kwargs):
    #     company = self.request.user.company
    #     threats = SWOTThreatOption.objects.filter(company=company)
    #     data = SWOTThreatOptionSerializer(threats, many=True).data
    #     return Response(data)
