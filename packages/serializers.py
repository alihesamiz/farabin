from packages.models import Package, Service

from rest_framework.serializers import ModelSerializer, SerializerMethodField, Serializer


class ServiceSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = ("id", "name", "description", "is_active")
        read_only_fields = ("id",)

class PackageSerializer(ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Package
        fields = ("id", "name", "description", "price", "period", "is_active", "services")
        read_only_fields = ("id",)

