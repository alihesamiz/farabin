import logging

from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from apps.company.models.company import CompanyUser
from apps.company.pagination import BasePagination
from apps.company.repositories import CompanyRepository as _repo
from apps.company.serializers import (
    CompanyProfileCreateSerializer,
    CompanyProfileSerializer,
    CompanyProfileUpdateSerializer,
    CompanyUserCreateSerializer,
    CompanyUserSerializer,
    CompanyUserUpdateSerializer,
    CompanyUserProfileSerializer,
)
from apps.company.services import CompanyService as _service
from apps.company.views import ViewSetMixin
from constants.responses import APIResponse

logger = logging.getLogger("company")

User = get_user_model()


class CompanyProfileViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {
        "list": CompanyProfileSerializer,
        "retrieve": CompanyProfileSerializer,
        "create": CompanyProfileCreateSerializer,
        "update": CompanyProfileUpdateSerializer,
        "partial_update": CompanyProfileUpdateSerializer,
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
        "add_user": CompanyUserProfileSerializer,
        "_": CompanyUserSerializer,
    }
    pagination_class = BasePagination

    def get_queryset(self):
        return _repo.get_company_user_for_company(company=self.get_company())

    @action(detail=False, methods=["post"], url_path="add")
    def add_user(self, request, *args, **kwargs):
        serializer = CompanyUserProfileSerializer(data=request.data)
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
