from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status


from packages.serializers import (
    OrderCreateSerializer,
    OrderSerializer,
    PackageSerializer,
    ServiceSerializer,
    SubscriptionSerializer,
)
from packages.models import (Order, Package, Service, Subscription,)


class ServiceViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ServiceSerializer
    http_method_names = ["get"]
    queryset = Service.objects.all()


class PackageViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PackageSerializer
    http_method_names = ["get"]
    queryset = Package.objects.all()


class SubscriptionsViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        return (
            Subscription.objects.select_related("package")
            .filter(user=user, is_active=True)
            .all()
        )

    @action(detail=False, methods=["get"], url_path="inactive")
    def inactive_subs(self, request):
        user = request.user
        inactive_subs = Subscription.objects.select_related("package").filter(
            user=user, is_active=False
        )
        serializer = self.get_serializer(inactive_subs, many=True)
        return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        status = self.request.query_params.get("status")
        if status not in dict(Order.OrderStatus.choices):
            status = Order.OrderStatus.PENDING_STATUS
        return Order.objects.filter(user=user, status=status).all()

    def get_serializer_class(self):
        if self.action == "create":
            return OrderCreateSerializer
        return OrderSerializer

    @action(detail=True, methods=["post"])
    def check_out(self, request, pk=None):
        order = self.get_object()
        order.set_as_paid()
        return Response({"message": "Order has been paid"}, status=status.HTTP_200_OK)
