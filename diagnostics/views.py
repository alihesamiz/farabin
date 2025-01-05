from itertools import groupby

from django.contrib.admin.views.decorators import staff_member_required
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.contrib.admin import site as admin_site
from django.core.cache import cache
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from .models import AnalysisReport, FinancialData
from company.models import CompanyProfile
from .serializers import (
    AgilityChartSerializer, AnalysisReportListSerializer, AnalysisReportSerializer, AssetChartSerializer, BankrupsyChartSerializer, CostChartSerializer, DebtChartSerializer, EquityChartSerializer, FinancialDataSerializer,
    InventoryChartSerializer, LeverageChartSerializer, LiquidityChartSerializer, FinancialDataSerializer, MonthDataSerializer,  ProfitChartSerializer, ProfitibilityChartSerializer, SalaryChartSerializer, SaleChartSerializer, YearlyFinanceDataSerializer
)


class DiagnosticAnalysisViewSet(ModelViewSet):

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

    http_method_names = ['get']

    permission_classes = [IsAuthenticated]

    serializer_class = FinancialDataSerializer

    def get_serializer_class(self):

        if self.action == "month":
            return YearlyFinanceDataSerializer

        elif self.action in ["chart", "chart_month"]:
            chart = self.kwargs.get('slug')

            serializer_class = self.CHART_SERIALIZER_MAP.get(chart)

            if serializer_class is None:
                raise NotFound(
                    detail=f"No serializer found for slug '{chart}'.")

            return serializer_class

        return super().get_serializer_class()

    def get_queryset(self):
        company = self.request.user.company

        cache_key = f"diagnostic_data_{company.id}"

        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data
        try:
            queryset = FinancialData.objects.select_related('financial_asset').filter(
                financial_asset__company=company,
                financial_asset__is_tax_record=True,
                is_published=True
            ).order_by('financial_asset__year', 'financial_asset__month')

            cache.set(cache_key, queryset)

            if not queryset.exists():
                raise NotFound(detail="No financial data found.")

            return queryset

        except Exception as e:
            raise NotFound(detail=f"Error retrieving financial data.{
                           e}", code=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='analysis', url_name='analysis')
    def analysis(self, request):
        company = self.request.user.company
        data_cache_key = f"diagnostic_analysis_{company.id}"
        cached_data = cache.get(data_cache_key)

        if cached_data:
            analysis = cached_data

        else:
            analysis = AnalysisReport.objects.select_related("calculated_data")\
                .prefetch_related("calculated_data__financial_asset")\
                .filter(
                calculated_data__financial_asset__company=company,
                calculated_data__is_published=True
                # Order by date (latest first)
            ).order_by('calculated_data__financial_asset__year', 'calculated_data__financial_asset__month', '-created_at')
            cache.set(data_cache_key, analysis)
        
        cache_key = f"diagnostic_analysis_data_{company.id}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        monthly_analysis = [
            item for item in analysis if item.calculated_data.financial_asset.is_tax_record is False]

        yearly_analysis = [
            item for item in analysis if item.calculated_data.financial_asset.is_tax_record is True]

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
            if topic in self.CHART_SERIALIZER_MAP:  # Ensure the chart is one of the valid topics
                monthly_serializer_data[topic] = AnalysisReportListSerializer(
                    item).data

        for topic, item in yearly_topic_data.items():
            if topic in self.CHART_SERIALIZER_MAP:  # Ensure the chart is one of the valid topics
                yearly_serializer_data[topic] = AnalysisReportListSerializer(
                    item).data

        result={
            "monthly_analysis": monthly_serializer_data,
            "yearly_analysis": yearly_serializer_data
        }
        cache.set(cache_key, result)
        # Combine the results into a single response
        return Response(result)

    @action(detail=False, methods=['get'], url_path='chart/(?P<slug>[^/.]+)', url_name='chart')
    def chart(self, request, slug=None):
        company = self.request.user.company

        cache_key = f"diagnostic_analysis_chart_yearly_{slug}_{company.id}"

        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        queryset = FinancialData.objects.select_related('financial_asset').filter(
            financial_asset__company=company,
            financial_asset__is_tax_record=True,
            is_published=True
        ).order_by('financial_asset__year', 'financial_asset__month')

        if not queryset.exists():
            raise NotFound(detail="No financial data found.")

        try:
            serializer = self.get_serializer(queryset, many=True)

            cache.set(cache_key, serializer.data, 3600)

            return Response(serializer.data)

        except Exception as e:
            raise NotFound(detail="Error fetching data: {}".format(str(e)))

    @action(detail=False, methods=['get'], url_path='chart/(?P<slug>[^/.]+)/month', url_name='chart-month')
    def chart_month(self, request, slug=None):
        company = self.request.user.company

        cache_key = f"diagnostic_analysis_chart_monthly_{slug}_{company.id}"

        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        queryset = FinancialData.objects.select_related('financial_asset').filter(
            financial_asset__company=company,
            financial_asset__is_tax_record=False,
            is_published=True
        ).order_by('financial_asset__year', 'financial_asset__month')

        if not queryset.exists():
            raise NotFound(detail="No financial data found.")

        try:
            serializer = self.get_serializer(queryset, many=True)

            cache.set(cache_key, serializer.data, 3600)

            return Response(serializer.data)

        except Exception as e:
            raise NotFound(detail="Error fetching data: {}".format(str(e)))

    @action(detail=False, methods=['get'], url_path='month', url_name='month')
    def month(self, request):
        company = self.request.user.company

        queryset = FinancialData.objects.select_related('financial_asset').filter(
            financial_asset__company=company,
            financial_asset__is_tax_record=False,
            is_published=True
        ).order_by('financial_asset__year', 'financial_asset__month')

        if not queryset.exists():
            return Response({'detail': 'No monthly data found.'}, status=status.HTTP_404_NOT_FOUND)

        data_by_year = {
            year: list(month_data)
            for year, month_data in groupby(queryset, key=lambda x: x.financial_asset.year)
        }

        result = [
            {
                'year': year,
                'months': MonthDataSerializer(month_data, many=True).data
            }
            for year, month_data in data_by_year.items()
        ]

        return Response(result)


@method_decorator(staff_member_required, name='dispatch')
class CompanyFinancialDataView(View):
    def get(self, request, company_id):

        company = CompanyProfile.objects.get(id=company_id)

        cache_key = f"company_admin_financial_data_{company_id}"
        cached_data = cache.get(cache_key)

        if cached_data:
            financial_data = cached_data

        financial_data = FinancialData.objects.select_related("financial_asset").filter(
            financial_asset__company=company).order_by('financial_asset__year', 'financial_asset__month')

        cache.set(cache_key, financial_data)

        admin_context = admin_site.each_context(request)
        admin_context['breadcrumbs'] = [
            {"name": _("Home"), "url": reverse('admin:index')},

            {"name": _("Diagnostic"), "url": '/admin/diagnostics/'},

            {"name": _("Analysis Reports"), "url": reverse(
                'admin:diagnostics_analysisreport_changelist')},

            {"name": company.company_title, "url": ""},

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
            month.append(float(data.financial_asset.month)
                         if data.financial_asset.month else '')
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
            equity_per_total_debt_ratio.append(float(
                data.equity_per_total_debt_ratio))
            equity_per_total_non_current_asset_ratio.append(float(
                data.equity_per_total_non_current_asset_ratio))
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

        return render(request, 'diagnostics/company_financial_data.html', {
            'company': company,
            'financial_data': financial_data,
            'year': year,
            'month': month,
            'net_sale': net_sale,
            'non_current_asset': non_current_asset,
            'current_asset': current_asset,
            'total_asset': total_asset,
            'non_current_debt': non_current_debt,
            'current_debt': current_debt,
            'total_debt': total_debt,
            'altman_bankrupsy_ratio': altman_bankrupsy_ratio,
            'total_equity': total_equity,
            'total_sum_equity_debt': total_sum_equity_debt,
            'inventory': inventory,
            'salary_fee': salary_fee,
            'production_fee': production_fee,
            'salary_production_fee': salary_production_fee,
            'roa': roa,
            'roab': roab,
            'roe': roe,
            'efficiency': efficiency,
            'gross_profit_margin': gross_profit_margin,
            'profit_margin_ratio': profit_margin_ratio,
            'debt_ratio': debt_ratio,
            'capital_ratio': capital_ratio,
            'proprietary_ratio': proprietary_ratio,
            'equity_per_total_debt_ratio': equity_per_total_debt_ratio,
            'equity_per_total_non_current_asset_ratio': equity_per_total_non_current_asset_ratio,
            'instant_ratio': instant_ratio,
            'current_ratio': current_ratio,
            'stock_turnover': stock_turnover,
            'gross_profit': gross_profit,
            'operational_profit': operational_profit,
            'proceed_profit': proceed_profit,
            'net_profit': net_profit,
            'construction_overhead': construction_overhead,
            'consuming_material': consuming_material,
            'production_total_price': production_total_price,
            **admin_context,  # Include admin context for breadcrumbs
        })
