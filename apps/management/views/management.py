import logging
import os
from django.db.models import QuerySet
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

from apps.company.models import CompanyUser
from common import ViewSetMixin
from constants.errors import ObjectNotFoundError
from apps.management.models import PersonelInformation
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated
from apps.management.models import OrganizationChartBase, HumanResource

from django.utils import timezone
from drf_spectacular.utils import extend_schema





logger = logging.getLogger("management")



from ..models import PersonelInformation
from apps.company.models import CompanyUser
from ..serializers import PersonelInformationSerializer
from apps.management.repositories import ManagementRepository as _repo








class PersonelInformationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]  # Require authentication
    serializer_class = PersonelInformationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            try:
                company = CompanyUser.objects.get(user=user).company
                return PersonelInformation.objects.filter(human_resource__company=company)
            except CompanyUser.DoesNotExist:
                return PersonelInformation.objects.none()
        return PersonelInformation.objects.none()

    def perform_create(self, serializer):
        """Assign the current user's company HumanResource when creating personnel."""
        user = self.request.user
        try:
            company = CompanyUser.objects.get(user=user).company
        except CompanyUser.DoesNotExist:
            raise ValidationError({"error": "This user is not associated with any company."})

        human_resource = _repo.get_human_resource_record_of_company(company=company).first()
        if not human_resource:
            raise ValidationError({"error": "No HumanResource record exists for this company."})

        serializer.save(human_resource=human_resource)

    def perform_update(self, serializer):
        """Ensure human_resource is preserved when updating personnel."""
        instance = self.get_object()
        serializer.save(human_resource=instance.human_resource)



    # Override create to add custom response
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "code": status.HTTP_201_CREATED,
                "message": "Personnel created successfully.",
                "data": response.data
            },
            status=status.HTTP_201_CREATED
        )

    # Override update to add custom response
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {
                "code": status.HTTP_200_OK,
                "message": "Personnel updated successfully.",
                "data": response.data
            },
            status=status.HTTP_200_OK
        )

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Response(
            {
                "code": status.HTTP_200_OK,
                "message": "Personnel partially updated successfully.",
                "data": response.data
            },
            status=status.HTTP_200_OK
        )




class HumanResourceViewSet(ViewSetMixin, ModelViewSet):
    service_attr = ServiceName.MANAGEMENT
    default_serializer_class = HumanResourceSerializer
    action_serializer_class = {
        "create": HumanResourceCreateSerializer,
        "update": HumanResourceUpdateSerializer,
        "partial_update": HumanResourceUpdateSerializer,
    }
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        company = self.get_company()
        if company is None:
            logger.warning("No company associated with user %s at %s", self.request.user, timezone.now())
            return HumanResource.objects.none()
        return _repo.get_human_resource_record_of_company(company=company)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["company"] = self.get_company()
        return context

    def perform_create(self, serializer):
        company = self.get_company()
        existing_records = _repo.get_human_resource_record_of_company(company=company)
        for record in existing_records:
            for field in record._meta.fields:
                if field.get_internal_type() == "FileField":
                    file_field = getattr(record, field.name)
                    if file_field and file_field.path and os.path.isfile(file_field.path):
                        os.remove(file_field.path)
            record.delete()
        try:
            serializer.save()
        except IntegrityError:
            raise ValidationError(
                {"error": _("Each company can only have one Human Resource record. To replace, you must first delete the previous record.")}
            )
        except Exception as e:
            logger.error(f"Error while saving new Human Resource record: {str(e)}")
            raise ValidationError(
                {"error": _("An error occurred while saving the Human Resource record.")}
            )

    def list(self, request, *args, **kwargs):
        company = self.get_company()
        if company is None:
            logger.warning("No company associated with user %s at %s", self.request.user, timezone.now())
            return Response(
                {"error": "No company associated with this user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        personnel = PersonelInformation.objects.filter(human_resource__company=company)
        if not personnel.exists():
            logger.info("No personnel found for company %s at %s", company, timezone.now())
            return Response(
                {"error": "No personnel found for your company."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PersonelInformationSerializer(personnel, many=True, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_200_OK)




    # Single peronel addition endpoint via Json format   
    @action(detail=False, methods=["post"], url_path="personnel", url_name="add-personnel")
    def add_personnel(self, request):
        """
        POST /management/human-resources/personnel/
        Add a single personnel record to the current user's company's HR.
        """
        user = request.user
        try:
            company_user = CompanyUser.objects.get(user=user)
            company = company_user.company
        except CompanyUser.DoesNotExist:
            return Response(
                {"error": "This user is not associated with any company."},
                status=status.HTTP_404_NOT_FOUND,
            )

        human_resource = _repo.get_human_resource_record_of_company(company=company).first()
        if not human_resource:
            return Response(
                {"error": "No HumanResource record exists for this company. Please create one first."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = PersonelInformationSerializer(data=request.data)
        if serializer.is_valid():
            personnel = serializer.save(human_resource=human_resource)
            return Response(
                PersonelInformationSerializer(personnel).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    

class OrganizationChartFileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrganizationChartFileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def get_company(self):
        """Return the user's company via CompanyUser or None."""
        user = self.request.user
        if user.is_anonymous:
            logger.warning("Anonymous user attempted access at 2025-08-28 12:30:00 +0400")
            logger.info("....")
            return None
        try:
            company_user = user.company_user
            if not company_user.company:
                logger.warning("User %s has no company associated via CompanyUser at 2025-08-28 12:30:00 +0400", 
                            user.phone_number)
                logger.info("....")
                return None
            return company_user.company
        except CompanyUser.DoesNotExist:
            logger.warning("User %s has no CompanyUser record at 2025-08-28 12:30:00 +0400", user.phone_number)
            logger.info("....")
            return None

    def get_queryset(self):
        """
        Return a QuerySet of organization chart files for the user's company.
        """
        try:
            company = self.get_company()
            if company is None:
                logger.warning("User %s has no company associated at 2025-08-28 12:06:00 +0400", self.request.user)
                logger.info("....")  # Separator
                return OrganizationChartBase.objects.none()

            queryset = _repo.get_base_chart_file_of_company(company=company)
            if queryset is None or not isinstance(queryset, QuerySet):
                logger.error("get_base_chart_file_of_company returned %s for company %s at 2025-08-28 12:06:00 +0400",
                             type(queryset), company)
                logger.info("....")  # Separator
                return OrganizationChartBase.objects.none()

            return queryset
        except Exception as e:
            logger.error("Error getting queryset for user %s: %s at 2025-08-28 12:06:00 +0400", self.request.user, str(e))
            logger.info("....")  # Separator
            return OrganizationChartBase.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            logger.info("No organization chart files found at 2025-08-28 12:06:00 +0400")
            logger.info("....")  # Separator
            return Response(
                {"error": "No organization chart file found for your company."},
                status=status.HTTP_404_NOT_FOUND,
            )
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=["GET"], url_name="download", url_path="download")
    def download(self, request):
        queryset = self.get_queryset().first()
        if not queryset:
            logger.warning("No associated OrganizationChart file found for user %s at 2025-08-28 12:06:00 +0400",
                          self.request.user)
            logger.info("....")  # Separator
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
