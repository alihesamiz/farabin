from rest_framework.permissions import SAFE_METHODS, BasePermission
from django.core.exceptions import ImproperlyConfigured

from constants.errors import NoCompanyAssignedError


class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        try:
            return request.user.company_user.role == "manager"
        except AttributeError:
            return False




class HasAccessToService(BasePermission):
    def has_permission(self, request, view):
        from apps.company.models import CompanyUser

        if not request.user or not request.user.is_authenticated:
            return False

        try:
            company_user = request.user.company_user
        except (NoCompanyAssignedError, CompanyUser.DoesNotExist):
            return False
        if not company_user.company:
            return False

        service_name = getattr(view, "service_attr", None)
        if not service_name:
            raise ImproperlyConfigured(
                f"{view.__class__.__name__} is missing the `service_attr` attribute."
            )
        company_has_service = company_user.company.services.filter(
            service__name=service_name, is_active=True, deleted_at__isnull=True
        ).exists()
        print(company_user.role)
        if not company_has_service:
            return False
        if company_user.role == CompanyUser.Role.MANAGER:
            return True
        return company_user.service_permissions.filter(
            service=service_name, deleted_at__isnull=True
        ).exists()


class Unautherized(BasePermission):
    def has_permission(self, request, view):
        return bool(not request.user or not request.user.is_authenticated)
