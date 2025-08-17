from apps.finance.models import TaxDeclarationFile
from apps.finance.models.finance import (
    AnalysisReport,
    BalanceReportFile,
    FinanceExcelFile,
    FinancialData,
)
from constants.typing import CompanyProfileType, ModelType, QuerySetType


class FinanceRepository:
    @staticmethod
    def get_available_years_for_file_model(
        company: CompanyProfileType, model: ModelType
    ) -> QuerySetType[ModelType]:
        base_queryset = model.objects.filter(company=company)

        if hasattr(model, "month"):
            return list(
                base_queryset.values_list("year", "month")
                .distinct()
                .order_by("year", "month")
            )
        else:
            return list(
                base_queryset.values_list("year", flat=True).distinct().order_by("year")
            )

    @staticmethod
    def get_tax_files_for_company(company: CompanyProfileType) -> ModelType:
        return (
            TaxDeclarationFile.objects.filter(company=company)
            .select_related("company")
            .order_by("-year")
        )

    @staticmethod
    def get_balance_report_files_for_company(company: CompanyProfileType) -> ModelType:
        return (
            BalanceReportFile.objects.filter(company=company)
            .order_by("-year", "month")
            .all()
        )

    @staticmethod
    def get_financial_excel_files_for_company(company: CompanyProfileType) -> ModelType:
        return FinanceExcelFile.objects.select_related("company").filter(
            company=company
        )

    # @staticmethod
    # def get_financial_data_for_company(company: CompanyProfileType) -> ModelType:
    #     return (
    #         FinancialData.objects.select_related("financial_asset")
    #         .prefetch_related("financial_asset__company")
    #         .filter(
    #             financial_asset__company=company,
    #             financial_asset__is_tax_record=True,
    #             is_published=True,
    #         )
    #         .order_by("financial_asset__year", "financial_asset__month")
    #     )

    @staticmethod
    def get_financial_data_for_company(
        company: CompanyProfileType, yearly: bool = False
    ) -> ModelType:
        return (
            FinancialData.objects.select_related("financial_asset")
            .prefetch_related("financial_asset__company")
            .filter(
                financial_asset__company=company,
                financial_asset__is_tax_record=yearly,
                is_published=True,
            )
            .order_by("financial_asset__year", "financial_asset__month")
        )

    @staticmethod
    def get_financial_analysis_for_company(company: CompanyProfileType) -> ModelType:
        return (
            AnalysisReport.objects.select_related("calculated_data")
            .prefetch_related("calculated_data__financial_asset")
            .filter(
                calculated_data__financial_asset__company=company,
                is_published=True,
            )
            .order_by(
                "chart_name",
                "-created_at",
                "calculated_data__financial_asset__year",
                "calculated_data__financial_asset__month",
            )
            # .distinct("chart_name")
        )

    @staticmethod
    def get_financial_charts_for_company(
        company: CompanyProfileType, yearly: bool = True
    ) -> ModelType:
        return (
            FinancialData.objects.select_related("financial_asset")
            .filter(
                financial_asset__company=company,
                financial_asset__is_tax_record=yearly,
                is_published=True,
            )
            .order_by("financial_asset__year", "financial_asset__month")
        )
