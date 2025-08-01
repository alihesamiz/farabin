from apps.salesdata.models import (
    CustomerSaleData,
    CustomerSaleFile,
    DomesticSaleData,
    DomesticSaleFile,
    ProductData,
    ProductDataFile,
    ProductLogFile,
)


class SaleRepository:
    @staticmethod
    def get_company_data(model, company):
        return model.objects.select_related("company").filter(company=company)

    @classmethod
    def get_product_for_company(cls, company):
        return cls.get_company_data(ProductData, company)

    @classmethod
    def get_customers_of_company(cls, company):
        return cls.get_company_data(CustomerSaleData, company)

    @classmethod
    def get_customers_file_of_company(cls, company, is_deleted: bool = True):
        is_deleted = is_deleted if is_deleted in [True, False] else True
        return cls.get_company_data(CustomerSaleFile, company).filter(
            deleted_at__isnull=is_deleted
        )

    @classmethod
    def get_product_logs_file_of_company(cls, company, is_deleted: bool = True):
        is_deleted = is_deleted if is_deleted in [True, False] else True
        return cls.get_company_data(ProductLogFile, company).filter(
            deleted_at__isnull=is_deleted
        )

    @classmethod
    def get_products_file_of_company(cls, company, is_deleted: bool = True):
        is_deleted = is_deleted if is_deleted in [True, False] else True
        return cls.get_company_data(ProductDataFile, company).filter(
            deleted_at__isnull=is_deleted
        )

    @classmethod
    def get_product_logs_of_company(cls, company, show_deleted: bool = False):
        qs = cls.get_company_data(ProductLogFile, company)

        if show_deleted:
            return qs.filter(deleted_at__isnull=False)

        return qs.filter(deleted_at__isnull=True)

    @classmethod
    def get_domestic_sale_of_company(cls, company):
        return cls.get_company_data(DomesticSaleData, company)

    classmethod

    def get_domestic_sale_file_of_company(cls, company):
        return cls.get_company_data(DomesticSaleFile, company)
