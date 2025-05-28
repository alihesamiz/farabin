from openai import OpenAIError
from pydantic import BaseModel, ValidationError
from google import genai

from collections import defaultdict
from openpyxl import load_workbook
from celery import shared_task
import logging

from django.db.transaction import atomic
from django.conf import settings

from apps.management.models import (
    HumanResource,
    PersonelInformation,
    SWOTMatrix,
    SWOTAnalysis,
    Position,
)


logger = logging.getLogger("management")


@shared_task(
    bind=True,
)
def process_personnel_excel(self, id: int):
    try:
        hr_instance = HumanResource.objects.get(id=id)
        file_path = hr_instance.excel_file.path
        company_name = hr_instance.company.company_title

        logger.info(f"Processing Excel file for company: {company_name}")
        logger.info(f"Loading workbook from {file_path}")

        wb = load_workbook(file_path)
        sheet = wb.active

        logger.info(f"Loading rows of data from {company_name} excel")

        personnel_list = []
        position_map = {}  # Maps position to list of PersonelInformation
        # Stores (person, reports_to_positions, cooperates_with_positions)
        person_relations = []

        for row in sheet.iter_rows(min_row=4, values_only=True):
            if not any(row):
                continue

            (
                name,
                position,
                reports_to_position,
                cooperates_with_position,
                obligations,
            ) = row[:5]

            if not (name and obligations and position):
                logger.warning(
                    f"Skipped invalid record: {name}, {obligations}, {position}. "
                    f"Missing reports_to {reports_to_position} or cooperates_with {cooperates_with_position}"
                )
                continue

            # Normalize data
            name = name.strip().title()
            position = position.strip().upper()
            is_exist = Position.objects.filter(position=position).exists()
            obligations = obligations.strip()
            reports_to_positions = (
                [p.strip().upper() for p in reports_to_position.strip().split(",")]
                if reports_to_position
                else []
            )
            cooperates_with_positions = (
                [p.strip().upper() for p in cooperates_with_position.strip().split(",")]
                if cooperates_with_position
                else []
            )

            person = PersonelInformation(
                human_resource=hr_instance,
                name=name,
                obligations=obligations,
                position=position,
                is_exist=is_exist,
            )
            personnel_list.append(person)

            # Store person in position_map (as a list)
            if position not in position_map:
                position_map[position] = []
            position_map[position].append(person)

            # Store relationships for later processing
            person_relations.append(
                (person, reports_to_positions, cooperates_with_positions)
            )

        with atomic():
            # Bulk create personnel
            created_personnel = PersonelInformation.objects.bulk_create(personnel_list)

            # Set many-to-many relationships
            for (
                person,
                reports_to_positions,
                cooperates_with_positions,
            ) in person_relations:
                # Set reports_to relationships
                for pos in reports_to_positions:
                    if pos in position_map:
                        person.reports_to.add(*position_map[pos])

                # Set cooperates_with relationships
                for pos in cooperates_with_positions:
                    if pos in position_map:
                        person.cooperates_with.add(*position_map[pos])

        logger.info(
            f"Successfully processed {len(created_personnel)} personnel records"
        )

    except HumanResource.DoesNotExist:
        logger.error(f"HumanResource with id {id} not found")
        raise
    except Exception as e:
        logger.error(f"Error processing Excel file: {str(e)}")
        raise


@shared_task(bind=True, rate_limit="5/m")
def generate_swot_analysis(self, id: int):
    try:

        class SWOTResponse(BaseModel):
            so: str
            st: str
            wo: str
            wt: str

        matrix_instance = SWOTMatrix.objects.get(id=id)

        logger.info(f"Creating SWOT analysis for {matrix_instance}")

        analysis_instance, created = SWOTAnalysis.objects.get_or_create(
            matrix=matrix_instance
        )
        analysis_groups = defaultdict(list)

        for option in matrix_instance.options.all():
            category = option.category[0].lower()
            index = len(analysis_groups[category])
            analysis_groups[category].append(
                f"{category.upper()}{index}: {option.answer}"
            )

        combinations_dict = {
            "so": analysis_groups["s"] + analysis_groups["o"],
            "st": analysis_groups["s"] + analysis_groups["t"],
            "wo": analysis_groups["w"] + analysis_groups["o"],
            "wt": analysis_groups["w"] + analysis_groups["t"],
        }

        prompt = f"""
    Create a detailed SWOT analysis in Persian language based on the following parameters provided. Present the output in a well-organized format with headings for each section.
        SWOT Parameters:
        Strengths,Opportunities: {combinations_dict["so"]}
        Strengths,Threats: {combinations_dict["st"]}
        Weaknesses,Opportunities: {combinations_dict["wo"]}
        Weaknesses,Threats: {combinations_dict["wt"]}

        Output Requirements:

        SWOT Matrix: Summarize the provided Strengths, Weaknesses, Opportunities, and Threats in a concise analysis.

        SO Strategies: Develop strategies that leverage Strengths to capitalize on Opportunities.
        ST Strategies: Develop strategies that use Strengths to mitigate Threats.
        WO Strategies: Develop strategies that address Weaknesses by taking advantage of Opportunities.
        WT Strategies: Develop strategies that minimize Weaknesses and avoid Threats.
        Ensure each strategy is specific, realistic, and tailored to the provided context.

        Use bullet points for clarity and include a brief explanation for each strategy.
    """

        try:
            client = genai.Client(api_key=settings.FARABIN_GEMINI_API_KEY)
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": SWOTResponse,
                },
            )
        except OpenAIError as genai_error:
            logger.error(f"LLM Error during content generation: {str(genai_error)}")
            raise genai_error

        try:
            analysis: SWOTResponse = response.parsed
        except ValidationError as val_err:
            logger.error(f"Response schema validation error: {val_err}")
            raise val_err

        # Populate the analysis instance safely
        analysis_instance.so = analysis.so or "N/A"
        analysis_instance.st = analysis.st or "N/A"
        analysis_instance.wo = analysis.wo or "N/A"
        analysis_instance.wt = analysis.wt or "N/A"
        analysis_instance.save()

        logger.info(f"SWOT analysis created for {matrix_instance}")

    except SWOTMatrix.DoesNotExist:
        error_msg = f"SWOTMatrix with id {id} does not exist."
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        logger.error(
            f"Unexpected error while creating SWOT analysis for {id}: {str(e)}"
        )
        return str(e)
