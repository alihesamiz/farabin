from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
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
from apps.salesdata.views.filters import CompanyDomesticSaleFilter
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
        query_param = self.request.query_params.get("show_deleted", "false").lower()
        show_deleted = query_param in ["true", "1", "t"]
        return _repo.get_product_for_company(company, show_deleted=show_deleted)


class CompanyProductFileViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {}

    default_serializer_class = CompanyProductFileSerializer
    ordering_fields = [
        "created_at",
        "updated_at",
    ]
    ordering = ["created_at"]

    def get_queryset(self):
        company = self.get_company()
        query_param = self.request.query_params.get("show_deleted", "false").lower()
        show_deleted = query_param in ["true", "1", "t"]
        return _repo.get_products_file_of_company(company, show_deleted=show_deleted)


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
        query_param = self.request.query_params.get("show_deleted", "false").lower()
        show_deleted = query_param in ["true", "1", "t"]
        return _repo.get_customers_of_company(company, show_deleted=show_deleted)


class CompanyCustomerFileViewSet(ViewSetMixin, ModelViewSet):
    # http_method_names = ["get", "post", "patch", "put"]
    action_serializer_class = {}
    default_serializer_class = CompanyCustomerFileSerializer
    ordering_fields = [
        "created_at",
        "updated_at",
    ]
    ordering = ["created_at"]

    def get_queryset(self):
        company = self.get_company()
        query_param = self.request.query_params.get("show_deleted", "false").lower()
        show_deleted = query_param in ["true", "1", "t"]
        return _repo.get_customers_file_of_company(company, show_deleted=show_deleted)


class CompanyProductLogViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {
        "list": CompanyProductLogListSerializer,
        "retrieve": CompanyProductLogSerializer,
        "create": CompanyProductLogCreateSerializer,
        "update": CompanyProductLogUpdateSerializer,
        "partial_update": CompanyProductLogUpdateSerializer,
    }
    search_fields = [
        "product_name",
    ]
    ordering = ["product_name", "production_date"]

    def get_queryset(self):
        company = self.get_company()
        query_param = self.request.query_params.get("show_deleted", "false").lower()
        show_deleted = query_param in ["true", "1", "t"]
        return _repo.get_product_logs_of_company(company, show_deleted)


class CompanyProductLogFileViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {}

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
        return _repo.get_product_logs_file_of_company(
            company, show_deleted=show_deleted
        )


class CompanyDomesticSaleViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {
        "list": CompanyDomesticSaleListSerializer,
        "retrieve": CompanyDomesticSaleSerializer,
        "create": CompanyDomesticSaleCreateSerializer,
        "update": CompanyDomesticSaleUpdateSerializer,
        "partial_update": CompanyDomesticSaleUpdateSerializer,
    }

    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = [
        "factor_number",
        "customer_name",
        "product_code",
        "product_name",
        "sold_amount",
        "sale_method",
        "payment_method",
    ]
    filterset_class = CompanyDomesticSaleFilter

    def get_queryset(self):
        company = self.get_company()
        query_param = self.request.query_params.get("show_deleted", "false").lower()
        show_deleted = query_param in ["true", "1", "t"]
        return _repo.get_domestic_sale_of_company(company, show_deleted=show_deleted)


class CompanyDomesticSaleFileViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {}

    default_serializer_class = CompanyDomesticSaleFileSerializer

    def get_queryset(self):
        company = self.get_company()
        query_param = self.request.query_params.get("show_deleted", "false").lower()
        show_deleted = query_param in ["true", "1", "t"]
        return _repo.get_domestic_sale_file_of_company(
            company, show_deleted=show_deleted
        )
