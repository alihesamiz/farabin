import logging
import os

from django.db.models.signals import post_save
from django.http import FileResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, ViewSet

from apps.company.models import ServiceName
from apps.finance.models import (
    BalanceReportFile,
    TaxDeclarationFile,
)
from apps.finance.repositories import FinanceRepository as _repo
from apps.finance.serializers import (
    AgilityChartSerializer,
    AnalysisReportListSerializer,
    AssetChartSerializer,
    BalanceReportRetrieveSerializer,
    BalanceReportSerializer,
    BankrupsyChartSerializer,
    CostChartSerializer,
    DebtChartSerializer,
    EquityChartSerializer,
    FinanceExcelFileSerializer,
    FinancialDataSerializer,
    InventoryChartSerializer,
    LeverageChartSerializer,
    LiquidityChartSerializer,
    ProfitChartSerializer,
    ProfitibilityChartSerializer,
    SalaryChartSerializer,
    SaleChartSerializer,
    TaxDeclarationRetrieveSerializer,
    TaxDeclarationSerializer,
)
from apps.finance.services.finance_service import FinanceService
from apps.finance.views.paginations import BasePagination
from common import ViewSetMixin
from constants.errors import (
    FinancialChartNameError,
    FinancialDataNotFoundError,
    NoQueryParameterError,
)
from constants.responses import APIResponse

logger = logging.getLogger("finance")


class TakenFileDateViewSet(ViewSetMixin, ViewSet):
    service_attr = ServiceName.FINANCIAL

    def list(self, request, *args, **kwargs):
        try:
            company = self.get_company()
            query_param = (
                self.request.query_params.get("file")
                if self.request.query_params.get("file") in ["tax", "balance"]
                else None
            )
            if query_param == "tax":
                years = _repo.get_available_years_for_file_model(
                    company=company, model=TaxDeclarationFile
                )
            elif query_param == "balance":
                years = _repo.get_available_years_for_file_model(
                    company=company, model=BalanceReportFile
                )
            return APIResponse.success(data=years)
        except UnboundLocalError:
            raise NoQueryParameterError


class TaxDeclarationViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {"retrieve": TaxDeclarationRetrieveSerializer}
    default_serializer_class = TaxDeclarationSerializer
    pagination_class = BasePagination
    service_attr = ServiceName.FINANCIAL

    def get_queryset(self):
        return _repo.get_tax_files_for_company(self.get_company())

    @xframe_options_exempt
    @action(detail=True, methods=["get"], url_path="pdf")
    def pdf(
        self,
        request,
        pk=None,
    ):
        tax_declaration = self.get_object()
        pdf_path = tax_declaration.file.path

        if not os.path.exists(pdf_path):
            logger.warning(
                "Requested PDF file not found",
                extra={"user_id": self.get_user().id, "file_id": pk},
            )
            return Response(
                {"error": "File not found"}, status=status.HTTP_404_NOT_FOUND
            )

        logger.info(
            "Serving PDF file", extra={"user_id": self.get_user().id, "file_id": pk}
        )
        response = FileResponse(open(pdf_path, "rb"), content_type="application/pdf")
        response["Content-Disposition"] = (
            f'inline; filename="{tax_declaration.file.name}"'
        )
        response["X-Frame-Options"] = "ALLOWALL"
        return response

    @action(detail=False, methods=["put", "patch"], url_path="send-experts")
    def send(self, request):
        """
        Update the 'is_sent' field to True for multiple TaxDeclaration instances.
        Expects a list of IDs in the request body.
        """
        user_id = self.get_user().id
        ids = request.data.get("ids", [])
        queryset = TaxDeclarationFile.objects.filter(
            id__in=ids, company=self.get_company()
        )

        updated_count = queryset.update(is_sent=True)
        instances = list(queryset)
        for instance in instances:
            post_save.send(sender=TaxDeclarationFile, instance=instance, created=False)

        logger.info(
            "Marked tax declarations as sent",
            extra={"user_id": user_id, "updated_count": updated_count},
        )

        return Response(
            {"success": f"{updated_count} files marked as sent."},
            status=status.HTTP_200_OK,
        )


class BalanceReportViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {"retrieve": BalanceReportRetrieveSerializer}
    default_serializer_class = BalanceReportSerializer
    pagination_class = BasePagination
    service_attr = ServiceName.FINANCIAL

    def get_queryset(self):
        return _repo.get_balance_report_files_for_company(self.get_company())

    @xframe_options_exempt
    @action(detail=True, methods=["get"], url_path="pdf")
    def pdf(self, request, pk=None):
        balance_report = self.get_object()
        file_name = request.query_params.get("file_name")

        if not file_name:
            return Response(
                {"error": "file_name query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        file_paths = {
            "balance_report_file": balance_report.balance_report_file.path,
            "profit_loss_file": balance_report.profit_loss_file.path,
            "sold_product_file": balance_report.sold_product_file.path,
            "account_turnover_file": balance_report.account_turnover_file.path,
        }

        if file_name not in file_paths:
            return Response(
                {"error": f"File {file_name} is not valid."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        file_path = file_paths[file_name]
        if not os.path.exists(file_path):
            return Response(
                {"error": f"File {file_name} not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        response = FileResponse(open(file_path, "rb"), content_type="application/pdf")
        response["Content-Disposition"] = f'inline; filename="{file_name}.pdf"'
        response["X-Frame-Options"] = "ALLOWALL"
        return response

    @action(detail=False, methods=["put", "patch"], url_path="send-experts")
    def send(self, request):
        ids = request.data.get("ids", [])
        queryset = BalanceReportFile.objects.filter(
            id__in=ids, company=self.get_company()
        )

        if not queryset.exists():
            return Response(
                {"error": "No valid tax declarations found for the provided IDs."},
                status=status.HTTP_404_NOT_FOUND,
            )

        updated_count = queryset.update(is_saved=True, is_sent=True)
        for instance in queryset:
            post_save.send(sender=BalanceReportFile, instance=instance, created=False)
        return Response(
            {"success": f"{updated_count} files marked as sent."},
            status=status.HTTP_200_OK,
        )


class FinanceExcelViewSet(ViewSetMixin, ModelViewSet):
    default_serializer_class = FinanceExcelFileSerializer
    pagination_class = BasePagination
    service_attr = ServiceName.FINANCIAL

    def get_queryset(self):
        company = self.get_company()
        return _repo.get_financial_excel_files_for_company(company)


class FinancialDataViewSet(ViewSetMixin, ReadOnlyModelViewSet):
    default_serializer_class = FinancialDataSerializer
    service_attr = ServiceName.FINANCIAL

    def get_queryset(self):
        company = self.get_company()
        qs = _repo.get_financial_data_for_company
        yearly = self.request.query_params.get("yearly")
        qs = qs(company, False) if not yearly else qs(company, True)
        if qs.exists():
            return qs
        raise FinancialDataNotFoundError


class FinancialChartViewSet(ViewSetMixin, ReadOnlyModelViewSet):
    lookup_field = "slug"
    service_attr = ServiceName.FINANCIAL

    CHART_SERIALIZER_MAP = {
        "debt": DebtChartSerializer,
        "asset": AssetChartSerializer,
        "sale": SaleChartSerializer,
        "equity": EquityChartSerializer,
        "bankrupsy": BankrupsyChartSerializer,
        "profitability": ProfitibilityChartSerializer,
        "inventory": InventoryChartSerializer,
        "agility": AgilityChartSerializer,
        "liquidity": LiquidityChartSerializer,
        "leverage": LeverageChartSerializer,
        "cost": CostChartSerializer,
        "profit": ProfitChartSerializer,
        "salary": SalaryChartSerializer,
    }
    serializer_class = FinancialDataSerializer

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                slug = self.kwargs.get(self.lookup_field)
                serializer_class = self.CHART_SERIALIZER_MAP.get(slug)

                if serializer_class:
                    return serializer_class
                else:
                    raise FinancialChartNameError

            case _:
                return super().get_serializer_class()

    def get_queryset(self):
        company = self.get_company()
        qs = _repo.get_financial_charts_for_company
        yearly = self.request.query_params.get("yearly")
        qs = qs(company, False) if not yearly else qs(company, True)
        if qs.exists():
            return qs
        raise FinancialDataNotFoundError

    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            queryset, many=True, context=self.get_serializer_context()
        )

        return APIResponse.success(data=serializer.data)


class FinanceAnalysisSummaryViewSet(ViewSetMixin, ViewSet):
    CHART_SERIALIZER_MAP = {
        "debt": DebtChartSerializer,
        "asset": AssetChartSerializer,
        "sale": SaleChartSerializer,
        "equity": EquityChartSerializer,
        "bankrupsy": BankrupsyChartSerializer,
        "profitability": ProfitibilityChartSerializer,
        "inventory": InventoryChartSerializer,
        "agility": AgilityChartSerializer,
        "liquidity": LiquidityChartSerializer,
        "leverage": LeverageChartSerializer,
        "cost": CostChartSerializer,
        "profit": ProfitChartSerializer,
        "salary": SalaryChartSerializer,
    }
    service_attr = ServiceName.FINANCIAL

    def list(self, request, *args, **kwargs):
        service = FinanceService(self.get_company())
        summary_data = service.get_analysis_summary_data()

        monthly_serializer_data = {}
        for topic, item in summary_data["monthly_analysis"].items():
            if topic in self.CHART_SERIALIZER_MAP:
                monthly_serializer_data[topic] = AnalysisReportListSerializer(item).data

        yearly_serializer_data = {}
        for topic, item in summary_data["yearly_analysis"].items():
            if topic in self.CHART_SERIALIZER_MAP:
                yearly_serializer_data[topic] = AnalysisReportListSerializer(item).data

        response_data = {
            "monthly_analysis": monthly_serializer_data,
            "yearly_analysis": yearly_serializer_data,
        }

        return APIResponse.success(data=response_data)
