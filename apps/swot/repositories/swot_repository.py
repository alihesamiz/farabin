from typing import Type

from apps.swot.models import (
    SWOTAnalysis,
    SWOTCategory,
    SWOTMatrix,
    SWOTOption,
    SWOTQuestion,
)
from constants.typing import CompanyModelQuery, ModelType, QuerySet, QuerySetType


class SWOTRepository:
    @staticmethod
    def get_company_data(
        model: Type[ModelType], company: CompanyModelQuery
    ) -> QuerySetType:
        return model.objects.select_related("company").filter(company=company)

    @staticmethod
    def is_valid_swot_category(value: str) -> bool:
        return value in SWOTCategory.values

    @staticmethod
    def get_swot_options() -> QuerySet[SWOTOption]:
        return SWOTOption.objects.all()

    @staticmethod
    def get_swot_questions() -> QuerySet[SWOTQuestion]:
        return SWOTQuestion.objects.all()

    @classmethod
    def get_swot_matrix_of_company(
        cls, company: CompanyModelQuery
    ) -> QuerySet[SWOTMatrix]:
        return cls.get_company_data(SWOTMatrix, company).order_by("-created_at")

    @classmethod
    def get_swot_analysis_of_company(
        cls, company: CompanyModelQuery
    ) -> QuerySet[SWOTAnalysis]:
        return SWOTAnalysis.objects.select_related("matrix").filter(
            matrix__company=company
        )
