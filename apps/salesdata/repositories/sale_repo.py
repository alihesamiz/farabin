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
    def get_company_data(model: ModelType, company: CompanyProfileType):
        return model.objects.select_related("company").filter(company=company)

    @classmethod
    def get_product_for_company(cls, company: CompanyProfileType):
        return cls.get_company_data(ProductData, company)

    @classmethod
    def get_customers_of_company(cls, company: CompanyProfileType):
        return cls.get_company_data(CustomerSaleData, company)

    @classmethod
    def get_customers_file_of_company(
        cls, company: CompanyProfileType, is_deleted: bool = True
    ):
        is_deleted = is_deleted if is_deleted in [True, False] else True
        return cls.get_company_data(CustomerSaleFile, company).filter(
            deleted_at__isnull=is_deleted
        )

    @classmethod
    def get_product_logs_file_of_company(
        cls, company: CompanyProfileType, show_deleted: bool = False
    ):
        return cls.get_company_data(ProductLogFile, company).filter(
            deleted_at__isnull=not show_deleted
        )

    @classmethod
    def get_products_file_of_company(
        cls, company: CompanyProfileType, is_deleted: bool = True
    ):
        is_deleted = is_deleted if is_deleted in [True, False] else True
        return cls.get_company_data(ProductDataFile, company).filter(
            deleted_at__isnull=is_deleted
        )

    @classmethod
    def get_product_logs_of_company(
        cls, company: CompanyProfileType, show_deleted: bool = False
    ):
        return (
            ProductLog.objects.prefetch_related("product__company").filter(
                product__company=company
            )
        ).filter(deleted_at__isnull=not show_deleted)

    @classmethod
    def get_domestic_sale_of_company(cls, company: CompanyProfileType):
        return cls.get_company_data(DomesticSaleData, company)

    classmethod

    def get_domestic_sale_file_of_company(cls, company: CompanyProfileType):
        return cls.get_company_data(DomesticSaleFile, company)
