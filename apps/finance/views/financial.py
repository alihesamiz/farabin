import logging
import os
from itertools import groupby

from django.contrib.admin import site as admin_site
from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from django.core.files.storage import default_storage
from django.db.models.signals import post_save
from django.db.transaction import atomic
from django.http import FileResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.company.models import CompanyProfile
from apps.company.views import ViewSetMixin
from apps.finance.models import (
    BalanceReportFile,
    FinancialData,
    TaxDeclarationFile,
)
from apps.finance.repositories import FinanceRepository as _repo
from apps.finance.serializers import (
    AgilityChartSerializer,
    AnalysisReportListSerializer,
    AssetChartSerializer,
    BalanceReportCreateSerializer,
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
    MonthDataSerializer,
    ProfitChartSerializer,
    ProfitibilityChartSerializer,
    SalaryChartSerializer,
    SaleChartSerializer,
    TaxDeclarationCreateSerializer,
    TaxDeclarationSerializer,
    YearlyFinanceDataSerializer,
)

logger = logging.getLogger("finance")


class TaxDeclarationViewSet(ViewSetMixin, ModelViewSet):
    action_serializer_class = {
        "list": TaxDeclarationSerializer,
        "retrieve": TaxDeclarationSerializer,
        "create": TaxDeclarationCreateSerializer,
        "update": TaxDeclarationCreateSerializer,
        "partial_update": TaxDeclarationCreateSerializer,
    }

    def get_queryset(self):
        return _repo.get_tax_files_for_company(self.get_company())

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context["request"] = self.request
    #     return context

    def destroy(self, request, *args, **kwargs):
        user_id = self.get_user().id
        try:
            instance = self.get_object()
            file_id = instance.id

            self.perform_destroy(instance)
            logger.info(
                "File deleted successfully",
                extra={"user_id": user_id, "file_id": file_id},
            )
            return Response(
                {"success": "file deleted"}, status=status.HTTP_204_NO_CONTENT
            )

        except Exception as e:
            logger.error(
                "Failed to delete file",
                extra={"user_id": user_id, "error": str(e)},
                exc_info=True,
            )
            return Response(
                {"error": "Failed to delete file"}, status=status.HTTP_400_BAD_REQUEST
            )

    def perform_destroy(self, instance):
        try:
            file_path = instance.tax_file.path
            folder_path = os.path.dirname(file_path)
            if file_path and default_storage.exists(file_path):
                default_storage.delete(file_path)
            if folder_path and not os.listdir(folder_path):
                os.rmdir(folder_path)
            instance.delete()
            logger.info(
                "File and file path deleted successfully",
                extra={"file_id": instance.id},
            )

        except Exception as e:
            logger.error(
                "Failed to delete file or file path",
                extra={"file_id": instance.id, "error": str(e)},
                exc_info=True,
            )

    @xframe_options_exempt
    @action(detail=True, methods=["get"], url_path="pdf")
    def pdf(
        self,
        request,
        pk=None,
    ):
        tax_declaration = self.get_object()
        pdf_path = tax_declaration.tax_file.path

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
            f'inline; filename="{tax_declaration.tax_file.name}"'
        )
        response["X-Frame-Options"] = "ALLOWALL"
        return response

    @action(detail=False, methods=["get"])
    def year(self, request):
        # tax_declarations = self.get_queryset()
        years = list(self.get_queryset().values_list("year", flat=True).distinct())
        logger.info(
            "Fetched unique tax declaration years",
            extra={"user_id": self.get_user().id, "years_count": len(years)},
        )

        return Response(years, status=status.HTTP_200_OK)

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
    action_serializer_class = {
        "create": BalanceReportCreateSerializer,
        "update": BalanceReportCreateSerializer,
        "partial_update": BalanceReportCreateSerializer,
    }
    default_serializer_class = BalanceReportSerializer

    def get_queryset(self):
        return _repo.get_balance_report_files_for_company(self.get_company())

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

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

    def destroy(self, request, *args, **kwargs):
        try:
            with atomic():
                instance = self.get_object()
                self.perform_destroy(instance)
                logger.info(
                    f"Balance report {instance.id} deleted successfully by user {self.get_user().id}"
                )
                return Response(
                    {"success": "files deleted"}, status=status.HTTP_204_NO_CONTENT
                )

        except Exception as e:
            logger.error(
                f"Failed to delete balance report {instance.id} - User: {self.get_user().id}, Error: {e}",
                exc_info=True,
            )
            return Response(
                {"error": "Failed to delete files"}, status=status.HTTP_400_BAD_REQUEST
            )

    def perform_destroy(self, instance):
        try:
            with atomic():
                file_paths = [
                    instance.balance_report_file.path,
                    instance.profit_loss_file.path,
                    instance.sold_product_file.path,
                    instance.account_turnover_file.path,
                ]

                folder_path = os.path.dirname(file_paths[0])

                for file_path in file_paths:
                    if file_path and default_storage.exists(file_path):
                        default_storage.delete(file_path)

                if folder_path and not os.listdir(folder_path):
                    os.rmdir(folder_path)

                instance.delete()
                logger.info(
                    f"Balance report {instance.id} and all associated files deleted by user {self.self.get_user().id}"
                )

        except Exception as e:
            logger.error(
                f"Failed to delete balance report files {instance.id} - User: {self.self.get_user().id}, Error: {e}",
                exc_info=True,
            )

    @action(detail=False, methods=["get"])
    def year(self, request):
        balance_reports = self.get_queryset()
        year_month_data = {}
        for entry in balance_reports.values("year", "month").distinct():
            year = entry["year"]
            month = entry["month"]
            if year not in year_month_data:
                year_month_data[year] = []

            if month not in year_month_data[year]:
                year_month_data[year].append(month)

        formatted_data = [
            {"year": year, "months": sorted(months)}
            for year, months in year_month_data.items()
        ]
        return Response(formatted_data, status=status.HTTP_200_OK)

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

    def get_queryset(self):
        return _repo.get_financial_excel_files_for_company(self.get_company())


class FinanceAnalysisViewSet(ViewSetMixin, ModelViewSet):
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
    action_serializer_class = {
        "month": YearlyFinanceDataSerializer,
    }

    http_method_names = ["get"]

    default_serializer_class = FinancialDataSerializer

    def get_serializer_class(self):
        if self.action == "month":
            return YearlyFinanceDataSerializer
        # print(self.action)

        elif self.action in ["chart", "chart_month"]:
            chart = self.kwargs.get("slug")

            serializer_class = self.CHART_SERIALIZER_MAP.get(chart)

            if serializer_class is None:
                raise NotFound(detail=f"No serializer found for slug '{chart}'.")

            return serializer_class

        return super().get_serializer_class()

    def get_queryset(self):
        company = self.get_company()

        cache_key = f"finance_data_{company.id}"

        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data
        try:
            queryset = _repo.get_financial_data_for_company(self.get_company())

            cache.set(cache_key, queryset)

            if not queryset.exists():
                raise NotFound(detail="No financial data found.")

            return queryset

        except Exception as e:
            raise NotFound(
                detail=f"Error retrieving financial data.{e}",
                code=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=False, methods=["get"], url_path="analysis", url_name="analysis")
    def analysis(self, request):
        company = self.get_company()
        data_cache_key = f"finance_analysis_{company.id}"
        cached_data = cache.get(data_cache_key)

        if cached_data:
            analysis = cached_data

        else:
            analysis = _repo.get_financial_analysis_for_company(self.get_company())

            cache.set(data_cache_key, analysis)

        cache_key = f"finance_analysis_data_{company.id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        monthly_analysis = [
            item
            for item in analysis
            if item.calculated_data.financial_asset.is_tax_record is False
        ]

        yearly_analysis = [
            item
            for item in analysis
            if item.calculated_data.financial_asset.is_tax_record is True
        ]

        monthly_topic_data = {}

        yearly_topic_data = {}

        for item in monthly_analysis[::-1]:
            if item.chart_name not in monthly_topic_data:
                monthly_topic_data[item.chart_name] = item

        for item in yearly_analysis[::-1]:
            if item.chart_name not in yearly_topic_data:
                yearly_topic_data[item.chart_name] = item

        monthly_serializer_data = {}
        yearly_serializer_data = {}

        for topic, item in monthly_topic_data.items():
            if topic in self.CHART_SERIALIZER_MAP:
                monthly_serializer_data[topic] = AnalysisReportListSerializer(item).data

        for topic, item in yearly_topic_data.items():
            if topic in self.CHART_SERIALIZER_MAP:
                yearly_serializer_data[topic] = AnalysisReportListSerializer(item).data

        result = {
            "monthly_analysis": monthly_serializer_data,
            "yearly_analysis": yearly_serializer_data,
        }
        cache.set(cache_key, result)
        # Combine the results into a single response
        return Response(result)

    @action(
        detail=False,
        methods=["get"],
        url_path="chart/(?P<slug>[^/.]+)",
        url_name="chart",
    )
    def chart(self, request, slug=None):
        company = self.get_company()

        cache_key = f"finance_analysis_chart_yearly_{slug}_{company.id}"

        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        queryset = _repo.get_financial_charts_for_company(self.get_company(), True)

        if not queryset.exists():
            raise NotFound(detail="No financial data found.")

        try:
            serializer = self.get_serializer(queryset, many=True)

            cache.set(cache_key, serializer.data, 3600)

            return Response(serializer.data)

        except Exception as e:
            raise NotFound(detail="Error fetching data: {}".format(str(e)))

    @action(
        detail=False,
        methods=["get"],
        url_path="chart/(?P<slug>[^/.]+)/month",
        url_name="chart-month",
    )
    def chart_month(self, request, slug=None):
        company = self.get_company()

        cache_key = f"finance_analysis_chart_monthly_{slug}_{company.id}"

        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        queryset = _repo.get_financial_charts_for_company(self.get_company(), False)

        if not queryset.exists():
            raise NotFound(detail="No financial data found.")

        try:
            serializer = self.get_serializer(queryset, many=True)

            cache.set(cache_key, serializer.data, 3600)

            return Response(serializer.data)

        except Exception as e:
            raise NotFound(detail="Error fetching data: {}".format(str(e)))

    @action(detail=False, methods=["get"], url_path="month", url_name="month")
    def month(self, request):
        company = self.get_company()

        queryset = (
            FinancialData.objects.select_related("financial_asset")
            .filter(
                financial_asset__company=company,
                financial_asset__is_tax_record=False,
                is_published=True,
            )
            .order_by("financial_asset__year", "financial_asset__month")
        )

        if not queryset.exists():
            return Response(
                {"detail": "No monthly data found."}, status=status.HTTP_404_NOT_FOUND
            )

        data_by_year = {
            year: list(month_data)
            for year, month_data in groupby(
                queryset, key=lambda x: x.financial_asset.year
            )
        }

        result = [
            {"year": year, "months": MonthDataSerializer(month_data, many=True).data}
            for year, month_data in data_by_year.items()
        ]

        return Response(result)


@method_decorator(staff_member_required, name="dispatch")
class CompanyFinancialDataView(View):
    def get(self, request, company_id):
        company = CompanyProfile.objects.get(id=company_id)

        cache_key = f"company_admin_financial_data_{company_id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            financial_data = cached_data

        else:
            financial_data = (
                FinancialData.objects.select_related(
                    "financial_asset", "financial_asset__company"
                )
                .filter(financial_asset__company=company)
                .order_by("financial_asset__year", "financial_asset__month")
            )

        cache.set(cache_key, financial_data)

        admin_context = admin_site.each_context(request)
        admin_context["breadcrumbs"] = [
            {"name": _("Home"), "url": reverse("admin:index")},
            {"name": _("finance"), "url": "/admin/finance/"},
            {
                "name": _("Analysis Reports"),
                "url": reverse("admin:finance_analysisreport_changelist"),
            },
            {"name": company.title, "url": ""},
        ]

        year = []
        month = []
        net_sale = []
        non_current_asset = []
        current_asset = []
        total_asset = []
        non_current_debt = []
        current_debt = []
        total_debt = []
        altman_bankrupsy_ratio = []
        total_equity = []
        total_debt = []
        total_sum_equity_debt = []
        inventory = []
        salary_fee = []
        production_fee = []
        salary_production_fee = []
        roa = []
        roab = []
        roe = []
        usability = []
        efficiency = []
        gross_profit_margin = []
        profit_margin_ratio = []
        debt_ratio = []
        capital_ratio = []
        proprietary_ratio = []
        equity_per_total_debt_ratio = []
        equity_per_total_non_current_asset_ratio = []
        instant_ratio = []
        current_ratio = []
        stock_turnover = []
        gross_profit = []
        operational_profit = []
        proceed_profit = []
        net_profit = []
        construction_overhead = []
        consuming_material = []
        production_total_price = []

        for data in financial_data:
            year.append(float(data.financial_asset.year))
            month.append(
                float(data.financial_asset.month) if data.financial_asset.month else ""
            )
            net_sale.append(float(data.net_sale))
            non_current_asset.append(float(data.non_current_asset))
            current_asset.append(float(data.current_asset))
            total_asset.append(float(data.total_asset))
            non_current_debt.append(float(data.non_current_debt))
            current_debt.append(float(data.current_debt))
            altman_bankrupsy_ratio.append(float(data.altman_bankrupsy_ratio))
            total_equity.append(float(data.total_equity))
            total_debt.append(float(data.total_debt))
            total_sum_equity_debt.append(float(data.total_sum_equity_debt))
            inventory.append(float(data.inventory_average))
            salary_fee.append(float(data.salary_fee))
            production_fee.append(float(data.production_fee))
            salary_production_fee.append(float(data.salary_production_fee))
            roa.append(float(data.roa))
            roab.append(float(data.roab))
            roe.append(float(data.roe))
            usability.append(float(data.usability))
            efficiency.append(float(data.efficiency))
            gross_profit_margin.append(float(data.gross_profit_margin))
            profit_margin_ratio.append(float(data.profit_margin_ratio))
            debt_ratio.append(float(data.debt_ratio))
            capital_ratio.append(float(data.capital_ratio))
            proprietary_ratio.append(float(data.proprietary_ratio))
            equity_per_total_debt_ratio.append(float(data.equity_per_total_debt_ratio))
            equity_per_total_non_current_asset_ratio.append(
                float(data.equity_per_total_non_current_asset_ratio)
            )
            instant_ratio.append(float(data.instant_ratio))
            current_ratio.append(float(data.current_ratio))
            stock_turnover.append(float(data.stock_turnover))
            gross_profit.append(float(data.gross_profit))
            operational_profit.append(float(data.operational_profit))
            proceed_profit.append(float(data.proceed_profit))
            net_profit.append(float(data.net_profit))
            construction_overhead.append(float(data.construction_overhead))
            consuming_material.append(float(data.consuming_material))
            production_total_price.append(float(data.production_total_price))

        return render(
            request,
            "finance/company_financial_data.html",
            {
                "company": company,
                "financial_data": financial_data,
                "year": year,
                "month": month,
                "net_sale": net_sale,
                "non_current_asset": non_current_asset,
                "current_asset": current_asset,
                "total_asset": total_asset,
                "non_current_debt": non_current_debt,
                "current_debt": current_debt,
                "total_debt": total_debt,
                "altman_bankrupsy_ratio": altman_bankrupsy_ratio,
                "total_equity": total_equity,
                "total_sum_equity_debt": total_sum_equity_debt,
                "inventory": inventory,
                "salary_fee": salary_fee,
                "production_fee": production_fee,
                "salary_production_fee": salary_production_fee,
                "roa": roa,
                "roab": roab,
                "roe": roe,
                "efficiency": efficiency,
                "gross_profit_margin": gross_profit_margin,
                "profit_margin_ratio": profit_margin_ratio,
                "debt_ratio": debt_ratio,
                "capital_ratio": capital_ratio,
                "proprietary_ratio": proprietary_ratio,
                "equity_per_total_debt_ratio": equity_per_total_debt_ratio,
                "equity_per_total_non_current_asset_ratio": equity_per_total_non_current_asset_ratio,
                "instant_ratio": instant_ratio,
                "current_ratio": current_ratio,
                "stock_turnover": stock_turnover,
                "gross_profit": gross_profit,
                "operational_profit": operational_profit,
                "proceed_profit": proceed_profit,
                "net_profit": net_profit,
                "construction_overhead": construction_overhead,
                "consuming_material": consuming_material,
                "production_total_price": production_total_price,
                **admin_context,
            },
        )
