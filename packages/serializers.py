from rest_framework import serializers

from packages.models import Order, Package, Promotion, Service, Subscription


class ServiceSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="services-detail", read_only=True)

    class Meta:
        model = Service
        fields = (
            "id",
            "url",
            "name",
            "code_name",
            "description",
            "price",
            "period",
            "is_active",
        )
        read_only_fields = (
            "id",
            "price",
            "period",
            "code_name",
            "is_active",
        )


class PackageSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = (
            "id",
            "name",
            "description",
            "price",
            "code_name",
            "created_at",
            "updated_at",
            "period",
            "services",
            "is_active",
        )
        read_only_fields = (
            "id",
            "is_active",
        )


class SubscriptionSerializer(serializers.ModelSerializer):
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


class OrderSerializer(serializers.ModelSerializer):
    package = PackageSerializer(read_only=True)
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "status",
            "package",
            "services",
            "created_at",
            "coupon",
            "total_price",
        ]
        read_only_fields = ["status", "created_at",
                            "package", "services", "user"]


class OrderCreateSerializer(serializers.ModelSerializer):
    package_id = serializers.PrimaryKeyRelatedField(
        queryset=Package.objects.all(), source="package"
    )
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(), source="service"
    )
    coupon_id = serializers.PrimaryKeyRelatedField(
        queryset=Promotion.objects.all(), source="coupon"
    )

    class Meta:
        model = Order
        fields = ["id", "package_id", "service_id", "coupon_id"]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return Order.objects.create(**validated_data)
