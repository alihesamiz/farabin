import logging
import os


from django.utils.translation import gettext_lazy as _
from django.http import FileResponse
from django.db import IntegrityError


from rest_framework import serializers, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response


from management.serializers import (
    ChartNodeSerializer,
    HumanResourceSerializer,
    HumanResourceCreateSerializer,
    HumanResourceUpdateSerializer,
    PersonelInformationSerializer,
    PersonelInformationUpdateSerializer,
    PersonelInformationCreateSerializer,
    OrganizationChartFileSerializer,
    SWOTMatrixSerializer,
    SWOTOptionCreateSerializer,
    SWOTOptionSerializer,
    SWOTQuestionSerializer,
)

from management.models import (
    HumanResource,
    PersonelInformation,
    OrganizationChartBase,
    SWOTMatrix,
    SWOTQuestion,
    SWOTOption,
)
from management.paginations import (
    PersonelPagination,
    SWOTOptionPagination,
    SWOTQuestionPagination,
)
from management.utils import get_file_field

logger = logging.getLogger("management")


class HumanResourceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        company = self.request.user.company
        return HumanResource.objects.filter(company=company)

    def get_serializer_class(self):
        if self.action == "create":
            return HumanResourceCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return HumanResourceUpdateSerializer
        return HumanResourceSerializer

    def perform_create(self, serializer):
        try:
            logger.info("Attempting to save new Human Resource record.")
            serializer.save()
            logger.info("Human Resource record created successfully.")
        except IntegrityError:
            logger.error(
                "IntegrityError: Trying to create a second Human Resource record for the company."
            )
            raise ValidationError(
                {
                    "error": _(
                        "Each company can only have one Human Resource record. To replace, you must first delete the previous record."
                    )
                }
            )
        except Exception as e:
            logger.error(f"Error while saving new Human Resource record: {str(e)}")
            raise ValidationError(
                {
                    "error": _(
                        "An error occurred while saving the Human Resource record."
                    )
                }
            )


class PersonelInformationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = PersonelPagination

    def get_queryset(self):
        company = self.request.user.company

        human_resource_id = self.kwargs.get("human_resource_pk")

        if human_resource_id:
            logger.info(
                f"Fetching PersonelInformation for HumanResource ID: {human_resource_id}"
            )
            return PersonelInformation.objects.select_related("human_resource").filter(
                human_resource__id=human_resource_id, human_resource__company=company
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
                f"HumanResource ID {human_resource_id} not found for company {company.company_title}."
            )
            raise serializers.ValidationError(
                {
                    "human_resource": _(
                        "Invalid or missing HumanResource record for this company."
                    )
                }
            )

        logger.info(
            f"Creating PersonelInformation for HumanResource ID: {human_resource_id}"
        )
        serializer.save(human_resource=human_resource)


class OrganizationChartFileViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationChartFileSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        field = self.request.user.company.tech_field
        file_field = get_file_field(field)
        return OrganizationChartBase.objects.filter(field=file_field)

    @action(detail=False, methods=["GET"], url_name="download", url_path="download")
    def download(self, request):

        queryset = self.get_queryset().first()
        if not queryset:
            logger.warning(
                "No associated OrganizationChart file found for the user's profile."
            )
            return Response(
                {"error": _("Not found an associated file with your profile")},
                status=status.HTTP_404_NOT_FOUND,
            )

        file_path = queryset.position_excel.path
        company_name = request.user.company.company_title
        logger.info(
            f"Returning Excel file for company {company_name}. File path: {file_path}"
        )

        return FileResponse(
            open(file_path, "rb"),
            as_attachment=True,
            filename=os.path.basename(file_path),
        )


class ChartNodeViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ChartNodeSerializer

    def get_queryset(self):
        company = self.request.user.company
        return PersonelInformation.objects.prefetch_related(
            "human_resource__company"
        ).filter(human_resource__company=company)

    def list(self, request, *args, **kwargs):
        company = self.request.user.company
        data = PersonelInformation.grouped_chart_data(company)
        return Response(data)

    @action(detail=False, methods=["get"], url_name="positions", url_path="positions")
    def by_positions(self, request, *args, **kwargs):
        """
        Custom action that expects a query parameter 'positions' (comma-separated values).
        It returns a JSON response where each key is a position and the value is a list
        of personnel (serialized) who hold that position.

        Example request:
            GET /chartnodes/positions/?pos=Manager,Developer
        """
        positions_param = request.query_params.get("pos")
        if not positions_param:
            return Response(
                {"detail": "Query parameter 'positions' is required."}, status=400
            )

        positions = [pos.strip() for pos in positions_param.split(",")]

        queryset = self.get_queryset().filter(position__in=positions)

        grouped_personnel = {}
        for person in queryset:
            pos = person.position

            if pos not in grouped_personnel:
                grouped_personnel[pos] = []

            serialized_person = self.get_serializer(person).data
            grouped_personnel[pos].append(serialized_person)

        return Response(grouped_personnel)


class SWOTQuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = SWOTQuestionPagination
    serializer_class = SWOTQuestionSerializer
    queryset = SWOTQuestion.objects.all()
    http_method_names = ["get"]


class SWOTOptionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SWOTOptionSerializer
    pagination_class = SWOTOptionPagination

    def get_serializer_class(self):
        if self.action == "create":
            logger.debug("Using SWOTOptionCreateSerializer for creation.")
            return SWOTOptionCreateSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        company = self.request.user.company
        logger.info(f"Fetching SWOT Options for company: {company.company_title}")
        return SWOTOption.objects.filter(company=company)


class SWOTMatrixViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SWOTMatrixSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        company = self.request.user.company
        logger.info(f"Fetching SWOT Matrices for company: {company.company_title}")
        return SWOTMatrix.objects.prefetch_related("options").filter(company=company)
