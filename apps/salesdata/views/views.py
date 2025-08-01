from rest_framework.viewsets import ModelViewSet

from apps.salesdata.repositories import SaleRepository as _repo
from apps.salesdata.serializers import (
    CompanyCustomerCreateSerializer,
    CompanyCustomerFileSerializer,
    CompanyCustomerListSerializer,
    CompanyCustomerSerializer,
    CompanyCustomerUpdateSerializer,
    CompanyDomesticSaleCreateSerializer,
    CompanyDomesticSaleFileSerializer,
    CompanyDomesticSaleListSerializer,
    CompanyDomesticSaleSerializer,
    CompanyDomesticSaleUpdateSerializer,
    CompanyProductFileSerializer,
    CompanyProductLogCreateSerializer,
    CompanyProductLogFileSerializer,
    CompanyProductLogListSerializer,
    CompanyProductLogSerializer,
    CompanyProductLogUpdateSerializer,
    ProductCreateSerializer,
    ProductListSerializer,
    ProductSerializer,
    ProductUpdateSerializer,
)
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


class CompanyProductLogViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {
        "list": CompanyProductLogListSerializer,
        "retrieve": CompanyProductLogSerializer,
        "create": CompanyProductLogCreateSerializer,
        "update": CompanyProductLogUpdateSerializer,
        "partial_update": CompanyProductLogUpdateSerializer,
    }
    search_fields = [
        "product__name",
    ]
    ordering = ["product__name", "production_date"]

    def get_queryset(self):
        company = self.get_company()
        return _repo.get_product_logs_of_company(company)


class CompanyProductLogFileViewSet(ViewSetMixin, ModelViewSet):
    http_method_names = ["get", "post", "patch", "put"]
    action_serializer_class = {
        "list": CompanyProductLogFileSerializer,
        "retrieve": CompanyProductLogFileSerializer,
        "create": CompanyProductLogFileSerializer,
        "update": CompanyProductLogFileSerializer,
        "partial_update": CompanyProductLogFileSerializer,
    }
    default_serializer_class = CompanyProductLogFileSerializer
    ordering_fields = [
        "created_at",
        "updated_at",
    ]
    ordering = ["created_at"]

    def get_queryset(self):
        company = self.get_company()
        query_param = self.request.query_params.get("show_deleted", "false").lower()
        show_deleted = query_param in ["true", "1", "t"]
        return _repo.get_product_logs_of_company(company, show_deleted=show_deleted)


class CompanyDomesticSaleViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {
        "list": CompanyDomesticSaleListSerializer,
        "retrieve": CompanyDomesticSaleSerializer,
        "create": CompanyDomesticSaleCreateSerializer,
        "update": CompanyDomesticSaleUpdateSerializer,
        "partial_update": CompanyDomesticSaleUpdateSerializer,
    }

    def get_queryset(self):
        company = self.get_company()
        return _repo.get_domestic_sale_of_company(company)


class CompanyDomesticSaleFileViewSet(ViewSetMixin,ModelViewSet):
    # action_serializer_class
    default_serializer_class = CompanyDomesticSaleFileSerializer
    
    def get_queryset(self):
        company = self.get_company()
        return _repo.get_domestic_sale_file_of_company(company)