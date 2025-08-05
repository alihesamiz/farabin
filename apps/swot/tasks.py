import logging
from collections import defaultdict

from celery import shared_task
from django.conf import settings
from google import genai
from openai import OpenAIError
from pydantic import BaseModel, ValidationError

from apps.swot.models import (
    CompanySWOTOptionMatrix,
    CompanySWOTQuestionMatrix,
    SWOTOptionAnalysis,
    SWOTQuestionAnalysis,
)

logger = logging.getLogger("swot")


@shared_task(bind=True, rate_limit="5/m")
def generate_swot_analysis(self, type: str, id: int):
    class SWOTResponse(BaseModel):
        so: str
        st: str
        wo: str
        wt: str

    try:
        match type:
            case "question":
                matrix_instance = CompanySWOTQuestionMatrix.objects.get(id=id)
                analysis_instance, created = SWOTQuestionAnalysis.objects.get_or_create(
                    matrix=matrix_instance
                )
            case "option":
                matrix_instance = CompanySWOTOptionMatrix.objects.get(id=id)
                analysis_instance, created = SWOTOptionAnalysis.objects.get_or_create(
                    matrix=matrix_instance
                )
            case _:
                ...
        logger.info(f"Creating SWOT analysis for {matrix_instance}")

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

    except CompanySWOTQuestionMatrix.DoesNotExist:
        error_msg = f"CompanySWOTQuestionMatrix with id {id} does not exist."
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        logger.error(
            f"Unexpected error while creating SWOT analysis for {id}: {str(e)}"
        )
        return str(e)
