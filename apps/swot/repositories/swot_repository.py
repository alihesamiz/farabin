from typing import Type

from django.db.models import Prefetch

from apps.swot.models import (
    CompanySWOTOption,
    CompanySWOTOptionAnalysis,
    CompanySWOTOptionMatrix,
    CompanySWOTQuestion,
    CompanySWOTQuestionAnalysis,
    CompanySWOTQuestionMatrix,
    SWOTCategory,
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
    def get_swot_options_of_company(
        cls, company: CompanyModelQuery, category: str
    ) -> QuerySet[CompanySWOTOption]:
        qs = cls.get_company_data(CompanySWOTOption, company)

        if category and cls.is_valid_swot_category(category):
            option_qs = SWOTOption.objects.filter(category=category)
            qs = qs.prefetch_related(Prefetch("options", queryset=option_qs))
        else:
            qs = qs.prefetch_related("options")

        return qs

    @classmethod
    def get_swot_questions_of_company(
        cls, company: CompanyModelQuery, category: str
    ) -> QuerySet[CompanySWOTQuestion]:
        qs = cls.get_company_data(CompanySWOTQuestion, company).select_related(
            "question"
        )
        if cls.is_valid_swot_category(category):
            qs = qs.filter(question__category=category)
        return qs

    @classmethod
    def get_swot_questions_matrix_of_company(
        cls, company: CompanyModelQuery, category: str
    ) -> QuerySet[CompanySWOTQuestionMatrix]:
        if cls.is_valid_swot_category(category):
            return CompanySWOTQuestionMatrix._filter_by_category(category).filter(
                company=company
            )
        return cls.get_company_data(CompanySWOTQuestionMatrix, company)

    @classmethod
    def get_swot_options_matrix_of_company(
        cls, company: CompanyModelQuery, category: str
    ) -> QuerySet[CompanySWOTQuestionMatrix]:
        if cls.is_valid_swot_category(category):
            return CompanySWOTOptionMatrix._filter_by_category(category).filter(
                company=company
            )
        return cls.get_company_data(CompanySWOTOptionMatrix, company)

    @classmethod
    def get_swot_question_analysis_of_company(
        cls, company: CompanyModelQuery
    ) -> QuerySet[CompanySWOTQuestionAnalysis]:
        return (
            CompanySWOTQuestionAnalysis.objects.filter(matrix__company=company)
            .select_related("matrix")
            .prefetch_related("matrix__company")
        )

    @classmethod
    def get_swot_option_analysis_of_company(
        cls, company: CompanyModelQuery
    ) -> QuerySet[CompanySWOTOptionAnalysis]:
        return (
            CompanySWOTOptionAnalysis.objects.filter(matrix__company=company)
            .select_related("matrix")
            .prefetch_related("matrix__company")
        )
