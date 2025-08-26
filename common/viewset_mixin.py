# from apps.company.models.profile import CompanyUserServicePermission
from django.utils import timezone

from apps.core.permissions import HasAccessToService
from constants.errors import (
    DatabaseSaveError,
    DeletionPermissionDenied,
    ObjectNotFoundError,
)
from constants.responses import APIResponse
from constants.typing import CompanyProfileType, UserType

 
class ViewSetMixin:
    service_attr = None  # Based on the viewset you are using, you should name the company user service permission choice in here
    permission_classes = [HasAccessToService]
    action_serializer_class = {
        "list": None,
        "retrieve": None,
        "create": None,
        "update": None,
        "partial_update": None,
    }
    default_serializer_class = None

    def get_company(self) -> CompanyProfileType:
        return self.request.user.company_user.company

    def get_user(self) -> UserType:
        return self.request.user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["company"] = self.get_company()
        context["user"] = self.get_user()
        return context

    def destroy(self, request, *args, **kwargs):
        """Implements a soft delete by setting the `deleted_at` field."""
        try: 
            instance = self.get_object()
            instance.deleted_at = timezone.now()
            instance.save()
            return APIResponse.no_content()
        except (DeletionPermissionDenied, DatabaseSaveError, ObjectNotFoundError) as e:
            return APIResponse.error(errors=e, code=e.status_code)

    def get_serializer_class(self):
        """Fetch the serializer class for the current action, or fallback to default."""
        return self.action_serializer_class.get(
            self.action, self.default_serializer_class
        )
