from typing import Type

from apps.swot.models import (
    SWOTCategory,
    SWOTModelMatrix,
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
    def get_swot_matrix(cls, company: CompanyModelQuery) -> QuerySet[SWOTModelMatrix]:
        return cls.get_company_data(SWOTModelMatrix, company).order_by("-created_at")
