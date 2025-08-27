from apps.salesdata.models import (
    CustomerSaleData,
    CustomerSaleFile,
    DomesticSaleData,
    DomesticSaleFile,
    ProductData,
    ProductDataFile,
    ProductLog,
    ProductLogFile,
)
from constants.typing import CompanyProfileType, ModelType


class SaleRepository:
    @staticmethod
    def get_company_data(
        model: ModelType, company: CompanyProfileType, show_deleted: bool = False
    ):
        show_deleted = show_deleted if show_deleted in [True, False] else True
        return model.objects.select_related("company").filter(
            company=company, deleted_at__isnull=not show_deleted
        )

    @classmethod
    def get_product_for_company(
        cls, company: CompanyProfileType, show_deleted: bool = False
    ):
        return cls.get_company_data(ProductData, company, show_deleted)

    @classmethod
    def get_customers_of_company(
        cls, company: CompanyProfileType, show_deleted: bool = False
    ):
        return cls.get_company_data(CustomerSaleData, company, show_deleted)

    @classmethod
    def get_customers_file_of_company(
        cls, company: CompanyProfileType, show_deleted: bool = False
    ):
        return cls.get_company_data(CustomerSaleFile, company, show_deleted)

    @classmethod
    def get_product_logs_file_of_company(
        cls, company: CompanyProfileType, show_deleted: bool = False
    ):
        return cls.get_company_data(ProductLogFile, company, show_deleted)

    @classmethod
    def get_products_file_of_company(
        cls, company: CompanyProfileType, show_deleted: bool = False
    ):
        show_deleted = show_deleted if show_deleted in [True, False] else True
        return cls.get_company_data(ProductDataFile, company, show_deleted)

    @classmethod
    def get_product_logs_of_company(
        cls, company: CompanyProfileType, show_deleted: bool = False
    ):
        return cls.get_company_data(ProductLog, company, show_deleted)

    @classmethod
    def get_domestic_sale_of_company(
        cls, company: CompanyProfileType, show_deleted: bool = False
    ):
        return cls.get_company_data(DomesticSaleData, company, show_deleted)

    classmethod

    def get_domestic_sale_file_of_company(
        cls, company: CompanyProfileType, show_deleted: bool = False
    ):
        return cls.get_company_data(DomesticSaleFile, company, show_deleted)
