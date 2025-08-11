# import pandas as pd
# from django.db.transaction import atomic

# from constants.typing import ModelType


class Reader:
    @staticmethod
    def process_domestic_file(instance_id: int):
        from apps.salesdata.tasks import read_domestic_file

        read_domestic_file.delay(instance_id)

    @staticmethod
    def process_customer_list_file(instance_id: int):
        from apps.salesdata.tasks import read_customer_list_file

        read_customer_list_file.delay(instance_id)

    @staticmethod
    def process_product_log_file(instance_id: int):
        from apps.salesdata.tasks import read_product_logs_file

        read_product_logs_file.delay(instance_id)

    @staticmethod
    def process_product_data_file(instance_id: int):
        from apps.salesdata.tasks import read_product_data_file

        read_product_data_file.delay(instance_id)


# TODO:to be tested
# class ExcelImporter:
#     def __init__(
#         self, model: ModelType, company_id: int, file_path: str, mappings: dict
#     ):
#         self.model = model
#         self.company_id = company_id
#         self.file_path = file_path
#         self.mappings = mappings

#     def _read_excel_to_dataframe(self, header_row: int) -> pd.DataFrame:
#         df = pd.read_excel(
#             self.file_path,
#             engine="openpyxl",
#             header=header_row,
#             usecols=lambda col: col != "ردیف",
#             dtype=str,
#         )
#         # Drop rows where all values are NaN
#         df.dropna(how="all", inplace=True)
#         return df

#     def _map_dataframe_to_objects(self, df: pd.DataFrame) -> list:
#         data_to_create = []
#         company = self.model.objects.get(pk=self.company_id) if self.model else None

#         for _, row in df.iterrows():
#             instance_data = {}
#             for excel_col, config in self.mappings.items():
#                 target_field = config["field"]
#                 value = row.get(excel_col)

#                 # Apply value mapping if defined
#                 if "map" in config:
#                     value = config["map"].get(value, config.get("default"))

#                 # Apply custom parsing function if defined
#                 if "parse_func" in config:
#                     value = config["parse_func"](value)

#                 instance_data[target_field] = value

#             # Add the company foreign key
#             if company:
#                 instance_data["company"] = company

#             data_to_create.append(self.model(**instance_data))

#         return data_to_create

#     def run_import(self, header_row: int):
#         try:
#             df = self._read_excel_to_dataframe(header_row)
#             objects_to_create = self._map_dataframe_to_objects(df)

#             with atomic():
#                 self.model.objects.bulk_create(objects_to_create)
#             return True
#         except Exception as e:
#             print(f"Import failed for model {self.model.__name__}: {e}")
#             return False
