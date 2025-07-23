from celery import shared_task

from apps.core.utils import ModelExcelReader

@shared_task(queue="high_priority")
def read_excel_file(file_path, company, model):
    create, msg = ModelExcelReader(model, company, file_path).create_instance()
    print(create, msg)
