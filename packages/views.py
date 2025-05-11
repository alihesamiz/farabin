from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action


from packages.serializers import (
    OrderCreateSerializer,
    OrderSerializer,
    PackageSerializer,
    ServiceSerializer,
    SubscriptionSerializer,
)
from packages.models import Order, Package, Service, Subscription


class ServiceViewSet(ModelViewSet):
    """
    >>> List the services
    """

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

    #
    #  Below is written with action which is not really aligned with RestFull APIs so the successive `query_params` are using.
    #
    # @action(methods=["get"], detail=False, url_path="confirmed")
    # def confirmed_orders(self, request):
    #     user = request.user
    #     confirmed_orders = Order.get_by_status(
    #         Order.OrderStatus.CONFIRMED_STATUS, user)
    #     serializer = self.get_serializer(confirmed_orders, many=True)
    #     return Response(serializer.data)

    # @action(methods=["get"], detail=False, url_path="canceled")
    # def canceled_orders(self, request):
    #     user = request.user
    #     canceled_orders = Order.get_by_status(
    #         Order.OrderStatus.CANCELED_STATUS, user)
    #     serializer = self.get_serializer(canceled_orders, many=True)
    #     return Response(serializer.data)

    # @action(methods=["get"], detail=False, url_path="paid")
    # def confirmed_orders(self, request):
    #     user = request.user
    #     confirmed_orders = Order.get_by_status(
    #         Order.OrderStatus.PAID_STATUS, user)
    #     serializer = self.get_serializer(confirmed_orders, many=True)
    #     return Response(serializer.data)
