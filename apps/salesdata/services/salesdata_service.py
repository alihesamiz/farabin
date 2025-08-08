from apps.core.utils import GeneralUtils
from constants.typing import ModelType


class SaleDataService:
    @classmethod
    def _get_upload_path(cls, instance: ModelType, filename: str, path: str) -> str:
        return GeneralUtils(path=path, fields=["company"]).rename_folder(
            instance, filename
        )

    @classmethod
    def set_domestic_data_file_upload_path(
        cls, instance: ModelType, filename: str
    ) -> str:
        return cls._get_upload_path(instance, filename, "sales_domestic_files")

    @classmethod
    def set_customer_data_file_upload_path(
        cls, instance: ModelType, filename: str
    ) -> str:
        return cls._get_upload_path(instance, filename, "sales_customer_files")

    @classmethod
    def set_product_data_file_upload_path(
        cls, instance: ModelType, filename: str
    ) -> str:
        return cls._get_upload_path(instance, filename, "sales_product_files")

    @classmethod
    def set_product_logs_file_upload_path(
        cls, instance: ModelType, filename: str
    ) -> str:
        return cls._get_upload_path(instance, filename, "sales_product_logs_files")
