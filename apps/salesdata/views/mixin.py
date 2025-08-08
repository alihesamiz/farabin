from rest_framework import filters
from rest_framework.serializers import Serializer

from apps.company.models.profile import CompanyUserServicePermission
from apps.core.permissions import HasAccessToService, IsManagerOrReadOnly
from apps.salesdata.views.pagination import BasePagination
from constants.typing import CompanyProfileType, UserType


class ViewSetMixin:
    service_attr = CompanyUserServicePermission.ServiceName.MARKETING
    permission_classes = [HasAccessToService | IsManagerOrReadOnly]
    action_serializer_class = {
        "list": r"Serializer Class Here",
        "retrieve": r"Serializer Class Here",
        "create": r"Serializer Class Here",
        "update": r"Serializer Class Here",
        "partial_update": r"Serializer Class Here",
    }
    default_serializer_class = Serializer
    pagination_class = BasePagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]

    def get_company(self) -> CompanyProfileType:
        return self.request.user.company_user.company

    def get_user(self) -> UserType:
        return self.request.user

    def get_serializer_class(self):
        serializer_class = self.action_serializer_class.get(self.action, None)
        if serializer_class is None:
            return self.default_serializer_class
        return serializer_class

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["company"] = self.get_company()
        return context
