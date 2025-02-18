from openpyxl import load_workbook
from celery import shared_task
import logging

from django.db.transaction import atomic


from management.models import HumanResource, PersonelInformation


logger = logging.getLogger("management")


@shared_task(bind=True)
def process_personnel_excel(self, id: int):
    try:
        hr_instance = HumanResource.objects.get(id=id)
        file_path = hr_instance.excel_file.path
        company_name = hr_instance.company.company_title

        logger.info(
            f"Processing Excel file for company: {company_name}")
        logger.info(f"Loading workbook from {file_path}")

        wb = load_workbook(file_path)
        sheet = wb.active

        logger.info(
            f"loading rows of data from {company_name} excel")

        personnel_list = []
        position_map = {}

        for row in sheet.iter_rows(min_row=4, values_only=True):
            if not any(row):
                continue

            name, unit, position, reports_to_position = row[:4]

            if not (name and unit and position):
                logger.warning(
                    f"Skipped invalid record: {name}, {unit}, {position}. Missing reports_to: {reports_to_position}"
                )
                continue

            person = PersonelInformation(
                human_resource=hr_instance,
                name=name.strip().title(),
                unit=unit.strip(),
                position=position.strip(),
                reports_to=None
            )
            personnel_list.append(person)
            position_map[position] = person

        
        with atomic():
            created_personnel = PersonelInformation.objects.bulk_create(
                personnel_list)

        
        updated_personnel = []
        for person in created_personnel:
            reports_to_position = next(
                (row[3] for row in sheet.iter_rows(min_row=4, values_only=True)
                 if row[2] == person.position), None
            )
            if reports_to_position and reports_to_position in position_map:
                person.reports_to = position_map[reports_to_position]
                updated_personnel.append(person)

        
        if updated_personnel:
            with atomic():
                PersonelInformation.objects.bulk_update(
                    updated_personnel, ["reports_to"])

        logger.info(
            f"Successfully processed and saved {len(created_personnel)} personnel records.")

    except Exception as e:
        logger.error(
            f"Error while processing the Excel file for company {company_name}: {str(e)}")
        return str(e)
