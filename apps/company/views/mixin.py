from rest_framework.serializers import Serializer

from apps.core.permissions import IsManagerOrReadOnly


class ViewSetMixin:
    """
    A reusable mixin for DRF ViewSets to dynamically assign serializers and permissions per action.

    Features:
    ---------
    - `permission_classes`: Default permission classes for the ViewSet. Can be overridden in subclasses.
    - `action_serializer_class`: A mapping of ViewSet actions (e.g., 'list', 'create', 'update') to their corresponding serializer classes.
    - `default_serializer_class`: A fallback serializer used if the current action does not have a specified serializer.

    Methods:
    --------
    - `get_serializer_class()`: Returns the serializer class for the current action.
      Falls back to `default_serializer_class` if the action is not in `action_serializer_class`.

    Usage:
    ------
    class MyViewSet(ViewSetMixin, ModelViewSet):
        permission_classes = [IsAdminUser]
        action_serializer_class = {
            "list": MyListSerializer,
            "retrieve": MyDetailSerializer,
            "create": MyCreateSerializer,
            "update": MyUpdateSerializer,
        }
        default_serializer_class = MyDefaultSerializer

    Notes:
    ------
    - If no serializer is defined for an action and `default_serializer_class` is not set,
      a `serializers.Serializer` will be used as the fallback.
    - Supports clean separation of serializers for read/write operations.

    """

    permission_classes = [IsManagerOrReadOnly]
    action_serializer_class = {
        "list": None,
        "retrieve": None,
        "create": None,
        "update": None,
        "partial_update": None,
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
