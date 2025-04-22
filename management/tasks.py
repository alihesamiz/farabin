from management.models import SWOTAnalysis
from openpyxl import load_workbook
from celery import shared_task
import logging

from django.db.transaction import atomic
from django.conf import settings

from management.models import HumanResource, PersonelInformation, SWOTMatrix

import cohere

logger = logging.getLogger("management")


@shared_task(bind=True,)
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

            name, position, reports_to_position, cooperates_with_position, obligations = row[
                :5]

            if not (name and obligations and position):
                logger.warning(
                    f"Skipped invalid record: {name}, {obligations}, {position}. Missing reports_to {reports_to_position} or cooperates_with {cooperates_with_position}")
                continue

            person = PersonelInformation(
                human_resource=hr_instance,
                name=name.strip().title(),
                obligations=obligations.strip(),
                position=position.strip(),
                reports_to=None,
                cooperates_with=None
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
            cooperates_with_position = next(
                (row[4] for row in sheet.iter_rows(min_row=5, values_only=True)
                 if row[2] == person.position), None
            )
            if cooperates_with_position and cooperates_with_position in position_map:
                person.cooperates_with = position_map[cooperates_with_position]
                updated_personnel.append(person)

        if updated_personnel:
            with atomic():
                PersonelInformation.objects.bulk_update(
                    updated_personnel, ["reports_to", "cooperates_with"])

        logger.info(
            f"Successfully processed and saved {len(created_personnel)} personnel records.")

    except Exception as e:
        logger.error(
            f"Error while processing the Excel file for company {company_name}: {str(e)}")
        return str(e)


@shared_task(bind=True, rate_limit='5/m')
def generate_swot_analysis(self, id: int):
    try:
        swot_instance = SWOTMatrix.objects.get(id=id)
        logger.info(f"Creating SWOT analysis for {swot_instance}")

        results = {}

        for field in ["strengths", "weaknesses", "opportunities", "threats"]:
            related_qs = getattr(swot_instance, field).values(
                "name", "custom_name")
            results[field] = [item["custom_name"] or item["name"]
                              for item in related_qs if item["custom_name"] or item["name"]]

        generator = cohere.ClientV2(settings.FARABIN_COHERE_API_KEY)
        prompt = f"""
        Provide the strategic and collision points for the SWOT matrix given the strengths, threats, opportunities, and weaknesses presented as below:
            Strengths: {results['strengths']}
            Weaknesses: {results['weaknesses']}
            Opportunities: {results['opportunities']}
            Threats: {results['threats']}
        this report and analysis should be in Persian language and a professional format and should be suitable for a business report.
        """
        response = generator.chat(
            model="command-r-plus",
            messages=[
                {
                    "role": "user",
                    "content": f"{prompt}"}],
        ).message.content[0].text

        SWOTAnalysis.objects.create(
            swot_matrix=swot_instance,
            analysis=response,
            is_approved=False
        )

        logger.info(f"SWOT analysis created for {swot_instance}")

    except Exception as e:
        logger.error(
            f"Error while creating SWOT analysis for {id}: {str(e)}")
        return str(e)
