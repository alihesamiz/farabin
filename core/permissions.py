from django.utils import timezone

from rest_framework.permissions import BasePermission

from packages.models import Subscription


class SubscriptionBasedPermission(BasePermission):
    def has_permission(self, request, view):
        # Define the required service or package for the ViewSet
        required_service = getattr(
            view, 'required_service', None)  # Set in ViewSet
        required_package = getattr(
            view, 'required_package', None)  # Set in ViewSet

        if not request.user.is_authenticated:
            return False

        # Check if the user has an active subscription that includes the required service or package
        active_subscriptions = Subscription.objects.filter(
            user=request.user,
            expires_at__gt=timezone.now()
        )

        if required_service:
            # Check if any active subscription's package includes the required service
            return active_subscriptions.filter(
                package__services__id=required_service.id
            ).exists()
        elif required_package:
            # Check if any active subscription is for the required package
            return active_subscriptions.filter(
                package__id=required_package.id
            ).exists()

        return False

    def has_object_permission(self, request, view, obj):
        # Optional: Add object-level checks (e.g., user can only edit their own subscriptions)
        if isinstance(obj, Subscription):
            return obj.user == request.user
        return self.has_permission(request, view)
