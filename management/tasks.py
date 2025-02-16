from openpyxl import load_workbook
from celery import shared_task
import logging
import os


from django.conf import settings


logger = logging.getLogger("management")


@shared_task()
def prepare_excel(company_name: str, file_path: str, action: str = "rename-column"):

    logger.info(
        f"Preparing Excel file for company: {company_name} with action: {action}")

    if action == "rename-column":
        try:
            logger.info(f"Loading workbook from {file_path}")

            wb = load_workbook(file_path)
            ws = wb.active

            logger.info(
                f"Renaming columns in the file for company: {company_name}")

            for col in ws.iter_cols(min_col=3, max_col=3, max_row=1):
                for cell in col:
                    original_value = cell.value
                    cell.value = cell.value.replace('x', company_name)
                    logger.debug(
                        f"Replaced '{original_value}' with '{cell.value}' in column {cell.column_letter}")

            new_filename = f"updated_{company_name}.xlsx"
            updated_file_path = os.path.join(
                settings.MEDIA_ROOT, "organization_charts", new_filename)

            os.makedirs(os.path.dirname(updated_file_path), exist_ok=True)
            logger.info(f"Saving updated file to {updated_file_path}")

            wb.save(updated_file_path)
            logger.info(
                f"File updated successfully for company: {company_name}")

            return updated_file_path

        except Exception as e:
            logger.error(
                f"Error while processing the Excel file for company {company_name}: {str(e)}")
            return str(e)
