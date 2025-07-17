from rest_framework.permissions import BasePermission, SAFE_METHODS


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
        except AttributeError:
            return False

        if company_user.role == CompanyUser.Role.MANAGER:
            return True

        service_name = getattr(view, "service_attr", None)
        if not service_name:
            return False

        return company_user.service_permissions.filter(
            service=service_name, deleted_at__isnull=True
        ).exists()


class Unautherized(BasePermission):
    def has_permission(self, request, view):
        return bool(not request.user or not request.user.is_authenticated)
