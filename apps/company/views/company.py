import logging

from django.contrib.auth import get_user_model
from django.db.models import Count

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.views import APIView

from constants.responses import APIResponse


from apps.company.models.profile import CompanyUser
from apps.company.views import ViewSetMixin
from apps.company.serializers import (
    CompanyProfileSerializer,
    CompanyUserSerializer,
    CompanyProfileCreateSerializer,
    # CompanyProfileUpdateSerializer,
    CompanyUserCreateSerializer,
    CompanyUserUpdateSerializer,
    UserProfileSerializer,
)

from apps.company.repositories import CompanyRepository as _repo
from apps.company.services import CompanyService as _service

from apps.finance.models.models import TaxDeclarationFile, BalanceReportFile
from apps.management.models import HumanResource

logger = logging.getLogger("company")

User = get_user_model()


class CompanyProfileViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {
        "list": CompanyProfileSerializer,
        "retrieve": CompanyProfileSerializer,
        "create": CompanyProfileCreateSerializer,
        "update": CompanyProfileCreateSerializer,
    }
    default_serializer_class = CompanyProfileSerializer

    def get_queryset(self):
        return _repo.get_company_for_user(user=self.get_user())


class CompanyUserViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {
        "list": CompanyUserSerializer,
        "retrieve": CompanyUserSerializer,
        "create": CompanyUserCreateSerializer,
        "update": CompanyUserUpdateSerializer,
        "partial_update": CompanyUserUpdateSerializer,
        "add_user": UserProfileSerializer,
        "_": CompanyUserSerializer,
    }

    def get_queryset(self):
        return _repo.get_company_user_for_company(company=self.get_company())

    @action(detail=False, methods=["post"], url_path="add")
    def add_user(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        role = request.data.get("role", CompanyUser.Role.STAFF)
        company = self.get_company()

        try:
            company_user = _service.add_user_to_company(
                company=company, validated_data=serializer.validated_data, role=role
            )
        except ValueError as e:
            return APIResponse.not_created(message=str(e))

        return APIResponse.created(
            data=CompanyUserSerializer(company_user).data, message="Company User added"
        )


class DashboardViewSet(ViewSetMixin, APIView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        company = self.get_company()

        if not company:
            return APIResponse.not_found(message="Company Profile not found")

        tax_file_count = TaxDeclarationFile.objects.filter(company=company).aggregate(
            tax_files_count=Count("id")
        )
        report_file_count = BalanceReportFile.objects.filter(company=company).aggregate(
            report_files_count=Count("id")
        )
        human_resource_count = HumanResource.objects.filter(company=company).aggregate(
            human_resource_files_count=Count("id")
        )

        # tickets_count = Ticket.objects.filter(issuer=company).count()

        total_uploaded_files_count = (
            tax_file_count["tax_files_count"]
            + report_file_count["report_files_count"]
            + human_resource_count["human_resource_files_count"]
        )

        response_data = {
            "all_uploaded_files_count": total_uploaded_files_count,
            "report_files_count": report_file_count["report_files_count"],
            "tax_files_count": tax_file_count["tax_files_count"],
            # "tickets_count": tickets_count,
        }

        return APIResponse.success(data=response_data)
