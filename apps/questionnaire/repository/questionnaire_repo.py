# In your repository file (e.g., apps/questionnaire/repositories.py)
from django.db import transaction
from django.db.models import QuerySet
from rest_framework.exceptions import ValidationError

from apps.questionnaire.models import (  # noqa: F401
    CompanyAnswer,
    CompanyQuestionnaire,
)
from constants.typing import CompanyProfileType




class QuestionnaireRepository:
    @staticmethod
    def get_company_questionnaires(
        company: CompanyProfileType,
    ) -> QuerySet[CompanyQuestionnaire]:
        return CompanyQuestionnaire.objects.select_related(
            "company", "questionnaire"
        ).filter(company=company)

    @staticmethod
    def get_company_questionnaire_detail(identifier: str) -> CompanyQuestionnaire:
        return (
            CompanyQuestionnaire.objects.select_related("questionnaire", "company")
            .prefetch_related(
                "answers__selected_choice",
                "questionnaire__questions__choices",
                "questionnaire__questions__metrics",
            )
            .get(questionnaire__id=identifier)  # direct string lookup
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


# class QuestionnaireRepository:
#     @staticmethod
#     def get_company_questionnaires(
#         company: CompanyProfileType,
#     ) -> QuerySet[CompanyQuestionnaire]:
#         return CompanyQuestionnaire.objects.select_related(
#             "company", "questionnaire"
#         ).filter(company=company)

#     @staticmethod
#     def get_company_questionnaire_detail(identifier: str) -> CompanyQuestionnaire:
#         """
#         Retrieve CompanyQuestionnaire either by PK (int) or by questionnaire.code (str like 'qs-01').
#         """
#         qs = (
#             CompanyQuestionnaire.objects.select_related("questionnaire", "company")
#             .prefetch_related(
#                 "answers__selected_choice",
#                 "questionnaire__questions__choices",
#                 "questionnaire__questions__metrics",
#             )
#         )

#         # # If identifier is int-like, fetch by pk
#         # if identifier.isdigit():
#         #     return qs.get(pk=int(identifier))

#         # Otherwise, assume it's a questionnaire code
#         #return qs.get(questionnaire__code=identifier)
#         return qs.get(questionnaire__id=identifier)




