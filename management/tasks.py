import os

from openpyxl import load_workbook

from django.conf import settings

from celery import shared_task


@shared_task()
def prepare_excel(company_name: str, file_path: str, action: str = "rename-column"):
    if action == "rename-column":
        try:
            wb = load_workbook(file_path)
            ws = wb.active

            for col in ws.iter_cols(min_col=3, max_col=3, max_row=1):
                for cell in col:
                    cell.value = cell.value.replace('x', company_name)

            new_filename = f"updated_{company_name}.xlsx"
            updated_file_path = os.path.join(
                settings.MEDIA_ROOT, "organization_charts", new_filename)

            os.makedirs(os.path.dirname(updated_file_path), exist_ok=True)

            wb.save(updated_file_path)

            return updated_file_path

        except Exception as e:
            return str(e)
