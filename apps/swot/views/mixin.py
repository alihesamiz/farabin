from apps.company.models import CompanyUserServicePermission
from apps.core.permissions import HasAccessToService
from constants.typing import CompanyModelQuery, ModelType


class ViewSetMixin:
    service_attr = CompanyUserServicePermission.ServiceName.MANAGEMENT
    permission_classes = [HasAccessToService]
    action_serializer_class = {
        "list": None,
        "retrieve": None,
        "create": None,
        "update": None,
        "partial_update": None,
    }
    default_serializer_class = None

    def get_company(self) -> CompanyModelQuery:
        return self.request.user.company_user.company

    def get_user(self) -> ModelType:
        return self.request.user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["company"] = self.get_company()
        return context

    def get_serializer_class(self):
        # Fetch the serializer class for the current action, or fallback to default
        serializer_class = self.action_serializer_class.get(self.action, None)
        if serializer_class is None:
            return self.default_serializer_class
        return serializer_class
