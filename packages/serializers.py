from django.db.models import Sum
from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, PrimaryKeyRelatedField, SerializerMethodField

from packages.models import Order, Package, Service, Subscription


class ServiceSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='services-detail', read_only=True)

    class Meta:
        model = Service
        fields = ("id", "url", "name",
                  "code_name",
                  "description",
                  "price",
                  "period",
                  "is_active")
        read_only_fields = ("id", "price", "period", "code_name", "is_active",)


class PackageSerializer(ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = ("id", "name",
                  "description",
                  "price",
                  "code_name",
                  "created_at",
                  "updated_at",
                  "period",
                  "services",
                  "is_active")
        read_only_fields = ("id", "is_active",)


class SubscriptionSerializer(ModelSerializer):
    package = PackageSerializer(read_only=True)
    service = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Subscription
        fields = [
            "id",
            "package",
            "service",
            "purchase_date",
            "expires_at",
            "duration",
        ]


class OrderSerializer(ModelSerializer):
    package = PackageSerializer(read_only=True)
    services = ServiceSerializer(many=True, read_only=True)
    total_price = SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "status",
            "package",
            "services",
            "total_price",
            "created_at"
        ]
        read_only_fields = ["status", "created_at",
                            "package", "services", "user"]

    def get_total_price(self, obj: Order):
        if obj.package:
            print("sadsad")
            return obj.package.price
        else:
            result = obj.service.aggregate(total=Sum("price"))
            print(result)
            return result["total"] or 0


class OrderCreateSerializer(ModelSerializer):
    package_id = PrimaryKeyRelatedField(
        queryset=Package.objects.all(), source="package"
    )
    service_id = PrimaryKeyRelatedField(
        queryset=Service.objects.all(), source="service"
    )

    class Meta:
        model = Order
        fields = ["id", "package_id", "service_id"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return Order.objects.create(**validated_data)
