from rest_framework.serializers import Serializer

from apps.core.permissions import IsManagerOrReadOnly
from constants.errors.api_exception import NoCompanyAssignedError
from constants.typing import CompanyProfileType, UserType


class ViewSetMixin:
    permission_classes = [IsManagerOrReadOnly]
    action_serializer_class = {
        "list": None,
        "retrieve": None,
        "create": None,
        "update": None,
        "partial_update": None,
    }
    default_serializer_class = Serializer

    def get_company(self) -> CompanyProfileType:
        try:
            return self.request.user.company_user.company
        except Exception:
            raise NoCompanyAssignedError()

    def get_user(self) -> UserType:
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
