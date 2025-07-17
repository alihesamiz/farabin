from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import Serializer


class ViewSetMixin:
    permission_classes = [IsAuthenticated]

    action_serializer_class = {
        "list": r"Serializer Class Here",
        "retrieve": r"Serializer Class Here",
        "create": r"Serializer Class Here",
        "update": r"Serializer Class Here",
        "partial_update": r"Serializer Class Here",
    }
    default_serializer_class = Serializer

    def get_company(self):
        return self.get_user().company_user.company

    def get_user(self):
        return self.request.user

    def get_serializer_class(self):
        # Fetch the serializer class for the current action, or fallback to default
        serializer_class = self.action_serializer_class.get(self.action, None)
        if serializer_class is None:
            return self.default_serializer_class
        return serializer_class
