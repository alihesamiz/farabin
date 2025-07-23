from rest_framework.viewsets import ModelViewSet


from apps.salesdata.serializers import (
    CompanyCustomerCreateSerializer,
    CompanyCustomerFileSerializer,
    CompanyCustomerListSerializer,
    CompanyCustomerSerializer,
    CompanyCustomerUpdateSerializer,
    CompanyProductFileSerializer,
    ProductListSerializer,
    ProductSerializer,
    ProductCreateSerializer,
    ProductUpdateSerializer,
)
from apps.salesdata.repositories import SaleRepository as _repo
from apps.salesdata.views.mixin import ViewSetMixin


class CompanyProductViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {
        "list": ProductListSerializer,
        "retrieve": ProductSerializer,
        "create": ProductCreateSerializer,
        "update": ProductUpdateSerializer,
        "partial_update": ProductUpdateSerializer,
    }
    ordering_fields = [
        "name",
        "code",
        "unit",
        "created_at",
        "updated_at",
    ]
    search_fields = [
        "name",
        "code",
    ]
    ordering = ["name"]

    def get_queryset(self):
        company = self.get_company()
        return _repo.get_product_for_company(company)


class CompanyProductFileViewSet(ViewSetMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "put"]
    action_serializer_class = {
        "list": CompanyProductFileSerializer,
        "retrieve": CompanyProductFileSerializer,
        "create": CompanyProductFileSerializer,
        "update": CompanyProductFileSerializer,
        "partial_update": CompanyProductFileSerializer,
    }
    default_serializer_class = CompanyProductFileSerializer
    ordering_fields = [
        "created_at",
        "updated_at",
    ]
    ordering = ["created_at"]

    def get_queryset(self):
        company = self.get_company()
        is_deleted = bool(self.request.query_params.get("is_deleted"))
        return _repo.get_products_file_of_company(company, is_deleted)


class CompanyCustomerViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {
        "list": CompanyCustomerListSerializer,
        "retrieve": CompanyCustomerSerializer,
        "create": CompanyCustomerCreateSerializer,
        "update": CompanyCustomerUpdateSerializer,
        "partial_update": CompanyCustomerUpdateSerializer,
    }
    ordering_fields = [
        "name",
        "sale_area",
        "channel",
        "city",
        "area",
        "first_purchase_date",
        "last_purchase_date",
    ]
    search_fields = [
        "name",
    ]
    ordering = ["name"]

    def get_queryset(self):
        company = self.get_company()
        return _repo.get_customers_of_company(company)


class CompanyCustomerFileViewSet(ViewSetMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "put"]
    action_serializer_class = {
        "list": CompanyCustomerFileSerializer,
        "retrieve": CompanyCustomerFileSerializer,
        "create": CompanyCustomerFileSerializer,
        "update": CompanyCustomerFileSerializer,
        "partial_update": CompanyCustomerFileSerializer,
    }
    default_serializer_class = CompanyCustomerFileSerializer
    ordering_fields = [
        "created_at",
        "updated_at",
    ]
    ordering = ["created_at"]

    def get_queryset(self):
        company = self.get_company()
        is_deleted = bool(self.request.query_params.get("is_deleted"))
        return _repo.get_customers_file_of_company(company, is_deleted)
