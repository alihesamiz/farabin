from rest_framework.serializers import Serializer

from apps.company.models.profile import CompanyUserServicePermission

from apps.core.permissions import HasAccessToService


class ViewSetMixin:
    service_attr = CompanyUserServicePermission.ServiceName.MANAGEMENT
    action_serializer_class = {
        "list": r"Serializer Class Here",
        "retrieve": r"Serializer Class Here",
        "create": r"Serializer Class Here",
        "update": r"Serializer Class Here",
        "partial_update": r"Serializer Class Here",
    }
    default_serializer_class = Serializer

    def get_company(self):
        return self.request.user.company_user.company

    def get_user(self):
        return self.request.user

    def get_serializer_class(self):
        return self.action_serializer_class.get(self.action, "_")

    permission_classes = [HasAccessToService]
