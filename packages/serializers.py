from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, PrimaryKeyRelatedField, SerializerMethodField

from packages.models import Order, Package, Service, Subscription

class ServiceSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(view_name='services-detail', read_only=True)

    class Meta:
        model = Service
        fields = ("id", "url", "name", "description", "is_active")
        read_only_fields = ("id", "is_active",)


class PackageSerializer(ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = ("id", "name", "description", "price",
                  "period", "is_active", "services")
        read_only_fields = ("id", "is_active",)


class SubscriptionSerializer(ModelSerializer):
    package = PackageSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = [
            "id",
            "package",
            "purchase_date",
            "expires_at",
            "duration",
        ]


class OrderSerializer(ModelSerializer):
    package = PackageSerializer(read_only=True)
    total_price = SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "status",
            "package",
            "total_price",
            "created_at"
        ]
        read_only_fields = ["status", "created_at", "package", "user"]

    def get_total_price(self, obj):
        return obj.package.price


class OrderCreateSerializer(ModelSerializer):
    package_id = PrimaryKeyRelatedField(
        queryset=Package.objects.all(), source="package"
    )

    class Meta:
        model = Order
        fields = ["id", "package_id"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return Order.objects.create(**validated_data)
