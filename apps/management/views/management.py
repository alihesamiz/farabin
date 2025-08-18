import logging
import os

from django.db import IntegrityError
from django.http import FileResponse
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from apps.company.models import ServiceName
from apps.management.paginations import (
    PersonnelPagination,
)
from apps.management.repositories import ManagementRepository as _repo
from apps.management.serializers import (
    ChartNodeSerializer,
    HumanResourceCreateSerializer,
    HumanResourceSerializer,
    HumanResourceUpdateSerializer,
    OrganizationChartFileSerializer,
    PersonelInformationCreateSerializer,
    PersonelInformationSerializer,
    PersonelInformationUpdateSerializer,
)
from common import ViewSetMixin
from constants.errors import ObjectNotFoundError

logger = logging.getLogger("management")


class HumanResourceViewSet(ViewSetMixin, ModelViewSet):
    service_attr = ServiceName.MANAGEMENT
    default_serializer_class = HumanResourceSerializer
    action_serializer_class = {
        "create": HumanResourceCreateSerializer,
        "update": HumanResourceUpdateSerializer,
        "partial_update": HumanResourceUpdateSerializer,
    }

    def get_queryset(self):
        return _repo.get_human_resource_record_of_company(company=self.get_company())

    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
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


class PersonnelInformationViewSet(ViewSetMixin, ModelViewSet):
    pagination_class = PersonnelPagination
    service_attr = ServiceName.MANAGEMENT

    default_serializer_class = PersonelInformationSerializer
    action_serializer_class = {
        "create": PersonelInformationCreateSerializer,
        "update": PersonelInformationUpdateSerializer,
        "partial_update": PersonelInformationUpdateSerializer,
    }

    def get_queryset(self):
        return _repo.get_personnel_info_of_company(company=self.get_company())

    def perform_create(self, serializer):
        company = self.get_company()

        human_resource_id = self.kwargs.get("human_resource_pk")
        human_resource = company.hrfiles.filter(id=human_resource_id).first()

        if not human_resource:
            raise ValidationError(
                {
                    "human_resource": _(
                        "Invalid or missing HumanResource record for this company."
                    )
                }
            )
        serializer.save(human_resource=human_resource)


class OrganizationChartFileViewSet(ViewSetMixin, ReadOnlyModelViewSet):
    default_serializer_class = OrganizationChartFileSerializer
    service_attr = ServiceName.MANAGEMENT

    http_method_names = ["get"]

    def get_queryset(self):
        return _repo.get_base_chart_file_of_company(company=self.get_company())

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

        return FileResponse(
            open(file_path, "rb"),
            as_attachment=True,
            filename=os.path.basename(file_path),
        )


class ChartNodeViewSet(ViewSetMixin, ReadOnlyModelViewSet):
    default_serializer_class = ChartNodeSerializer
    service_attr = ServiceName.MANAGEMENT

    def get_queryset(self):
        return _repo.get_personnel_info_of_company(company=self.get_company())

    def list(self, request, *args, **kwargs):
        data = _repo.get_personnel_info_grouped_chart_data(company=self.get_company())
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
        pos_param: str = request.query_params.get("pos")

        if not pos_param:
            return Response(
                {"detail": "Query parameter 'pos' is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Resolve position names if a numeric code is passed
        if pos_param.isdigit():
            try:
                pos_param = _repo.get_position_by_code(int(pos_param))
            except ObjectNotFoundError:
                return Response(
                    {"detail": f"No position found with code {pos_param}."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        positions = [p.strip() for p in pos_param.split(",") if p.strip()]

        if not positions:
            return Response(
                {"detail": "No valid positions found in 'pos' parameter."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Delegate to repository
        grouped_data = _repo.get_personnel_info_by_position(
            self.get_queryset(), self.get_serializer, positions
        )
        return Response(grouped_data, status=status.HTTP_200_OK)
