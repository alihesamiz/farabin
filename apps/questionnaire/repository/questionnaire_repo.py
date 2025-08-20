# In your repository file (e.g., apps/questionnaire/repositories.py)
from django.db import transaction
from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

from apps.questionnaire.models import (  # noqa: F401
    CompanyAnswer,
    CompanyQuestionnaire,
)
from constants.typing import CompanyProfileType

# Assuming your type hints are set up
# from typing import List, Dict, Any
# from your_apps import CompanyProfileType, UserType, CompanyQuestionnaire


class QuestionnaireRepository:
    @staticmethod
    def get_company_questionnaires(
        company: CompanyProfileType,
    ) -> QuerySet[CompanyQuestionnaire]:
        return CompanyQuestionnaire.objects.select_related(
            "company", "questionnaire"
        ).filter(company=company)

    @staticmethod
    def get_company_questionnaire_detail(pk: int) -> CompanyQuestionnaire:
        return (
            CompanyQuestionnaire.objects.select_related("questionnaire", "company")
            .prefetch_related(
                "answers__selected_choice",
                "questionnaire__questions__choices",
                "questionnaire__questions__metrics",
            )
            .get(pk=pk)
        )

    @staticmethod
    @transaction.atomic
    def bulk_create_or_update_answers(
        company_questionnaire: CompanyQuestionnaire, answers_data: list[dict]
    ) -> None:
        """
        Receives a list of answer data and creates or updates them for a
        given CompanyQuestionnaire instance. Runs in a single transaction.
        """
        question_ids = [item["question_id"] for item in answers_data]

        # Validate that all questions belong to this questionnaire
        valid_question_ids = set(
            company_questionnaire.questionnaire.questions.values_list("id", flat=True)
        )
        if not set(question_ids).issubset(valid_question_ids):
            raise ValidationError(
                "One or more questions do not belong to this questionnaire."
            )

        for answer_data in answers_data:
            question_id = answer_data.pop("question_id")
            selected_choice_id = answer_data.pop("selected_choice_id")

            # Using update_or_create handles both new and existing answers cleanly
            CompanyAnswer.objects.update_or_create(
                company_questionnaire=company_questionnaire,
                question_id=question_id,
                defaults={"selected_choice_id": selected_choice_id},
            )
