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


from management.serializers import (HumanResourceSerializer, HumanResourceCreateSerializer, HumanResourceUpdateSerializer,
                                    PersonelInformationSerializer, PersonelInformationUpdateSerializer, PersonelInformationCreateSerializer,
                                    OrganizationChartFileSerializer)
from management.models import HumanResource, PersonelInformation, OrganizationChartBase
from management.utils import check_file_ready, get_file_field
from management.paginations import PersonelPagination
from management.tasks import prepare_excel


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
        company = self.request.user.company
        field = company.tech_field
        file_field = get_file_field(field)
        return OrganizationChartBase.objects.filter(field=file_field)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().first()
        if not queryset:
            logger.warning("No associated OrganizationChart file found for the user's profile.")
            return Response({"error": _("Not found an associated file with your profile")}, status=status.HTTP_404_NOT_FOUND)

        file_path = queryset.position_excel.path
        company_name = request.user.company.company_title

        logger.info(f"Processing Excel file for company {company_name}. File path: {file_path}")
        task = prepare_excel.delay(
            company_name=company_name, file_path=file_path, action="rename-column")

        return Response(
            {
                "message": _("Processing started. Check back later for the file. Proceed to 'download' action for getting the file"),
                "download_url": f"/download/?company_name={company_name}",
                "task_id": task.id,
            },
            status=status.HTTP_202_ACCEPTED,
        )

    @action(detail=False, methods=['GET'], url_name='download', url_path='download')
    def download(self, request):
        """Check if the updated file exists and return it."""
        company_name = request.GET.get("company_name")
        if not company_name:
            logger.error("Company name is missing in the download request.")
            return Response({"error": _("Company name is required")}, status=status.HTTP_400_BAD_REQUEST)

        latest_file = check_file_ready(company_name)
        if isinstance(latest_file, Response):
            logger.error(f"Error checking file for company {company_name}: {latest_file.data}")
            return latest_file

        logger.info(f"Returning updated file for company {company_name}.")
        return FileResponse(open(latest_file, "rb"), as_attachment=True, filename=os.path.basename(latest_file))
