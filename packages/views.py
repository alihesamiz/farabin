from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import status


from packages.serializers import PackageSerializer, ServiceSerializer
from packages.models import Package, Service


class ServiceViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()


class PackageViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PackageSerializer
    http_method_names = ["get"]
    queryset = Package.objects.all()
