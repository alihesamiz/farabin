from apps.salesdata.models import (
    ProductData,
    CustomerSaleData,
    CustomerSaleFile,
    ProductDataFile,
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
    def get_products_file_of_company(cls, company, is_deleted: bool = True):
        is_deleted = is_deleted if is_deleted in [True, False] else True
        return cls.get_company_data(ProductDataFile, company).filter(
            deleted_at__isnull=is_deleted
        )
