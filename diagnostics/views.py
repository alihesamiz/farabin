from django.utils.decorators import method_decorator
from django.contrib.admin import site as admin_site
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import base64
import io
import matplotlib.pyplot as plt
from company.models import CompanyProfile
from django.views import View
from django.shortcuts import render
from typing import Any
from itertools import groupby
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from .serializers import (
    AgilityChartSerializer, AssetChartSerializer, BankrupsyChartSerializer, CostChartSerializer, DebtChartSerializer, EquityChartSerializer, FinancialAssetSerializer, FinancialDataSerializer,
    InventoryChartSerializer, LeverageChartSerializer, LiquidityChartSerializer, FinancialDataSerializer, MonthDataSerializer, MonthlyFinancialDataSerializer, ProfitChartSerializer, ProfitibilityChartSerializer, SaleChartSerializer, YearlyFinanceDataSerializer
)
from .models import FinancialData


class DiagnosticAnalysisViewSet(ModelViewSet):

    CHART_SERIALIZER_MAP = {
        "debt": DebtChartSerializer,
        "asset": AssetChartSerializer,
        "sale": SaleChartSerializer,
        "equity": EquityChartSerializer,
        "bankrupsy": BankrupsyChartSerializer,
        "profitibility": ProfitibilityChartSerializer,
        "inventory": InventoryChartSerializer,
        "agility": AgilityChartSerializer,
        "liquidity": LiquidityChartSerializer,
        "leverage": LeverageChartSerializer,
        "cost": CostChartSerializer,
        "profit": ProfitChartSerializer,
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
        queryset = FinancialData.objects.select_related('financial_asset').filter(
            financial_asset__company=company,
            financial_asset__is_tax_record=True,
            is_published=True
        )
        if not queryset.exists():
            raise NotFound(detail="No financial data found.")
        return queryset

    @action(detail=False, methods=['get'], url_path='chart/(?P<slug>[^/.]+)', url_name='chart')
    def chart(self, request, slug=None):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='chart/(?P<slug>[^/.]+)/month', url_name='chart-month')
    def chart_month(self, request, slug=None):
        company = self.request.user.company
        queryset = FinancialData.objects.select_related('financial_asset').filter(
            financial_asset__company=company,
            financial_asset__is_tax_record=False,
            is_published=True
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='month', url_name='month')
    def month(self, request):
        company = request.user.company
        queryset = FinancialData.objects.select_related('financial_asset').filter(
            financial_asset__company=company,
            financial_asset__is_tax_record=False,
            is_published=True
        )

        if not queryset.exists():
            return Response({'detail': 'No monthly data found.'}, status=status.HTTP_404_NOT_FOUND)

        # Group data by year
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
        # Fetch the company profile
        company = CompanyProfile.objects.get(id=company_id)

        financial_data = FinancialData.objects.filter(
            financial_asset__company=company).order_by('financial_asset__year', 'financial_asset__month')

        admin_context = admin_site.each_context(request)
        # admin_context['title'] = _("Company Financial Data")
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
            year.append(int(data.financial_asset.year))
            month.append(int(data.financial_asset.month)
                         if data.financial_asset.month else '')
            net_sale.append(int(data.net_sale))
            non_current_asset.append(int(data.non_current_asset))
            current_asset.append(int(data.current_asset))
            total_asset.append(int(data.total_asset))
            non_current_debt.append(int(data.non_current_debt))
            current_debt.append(int(data.current_debt))
            total_debt.append(int(data.total_debt))
            altman_bankrupsy_ratio.append(int(data.altman_bankrupsy_ratio))
            total_equity.append(int(data.total_equity))
            total_debt.append(int(data.total_debt))
            total_sum_equity_debt.append(int(data.total_sum_equity_debt))
            inventory.append(int(data.inventory))
            salary_fee.append(int(data.salary_fee))
            production_fee.append(int(data.production_fee))
            salary_production_fee.append(int(data.salary_production_fee))
            roa.append(int(data.roa))
            roab.append(int(data.roab))
            roe.append(int(data.roe))
            efficiency.append(int(data.efficiency))
            gross_profit_margin.append(int(data.gross_profit_margin))
            profit_margin_ratio.append(int(data.profit_margin_ratio))
            debt_ratio.append(int(data.debt_ratio))
            capital_ratio.append(int(data.capital_ratio))
            proprietary_ratio.append(int(data.proprietary_ratio))
            equity_per_total_debt_ratio.append(int(
                data.equity_per_total_debt_ratio))
            equity_per_total_non_current_asset_ratio.append(int(
                data.equity_per_total_non_current_asset_ratio))
            instant_ratio.append(int(data.instant_ratio))
            current_ratio.append(int(data.current_ratio))
            stock_turnover.append(int(data.stock_turnover))
            gross_profit.append(int(data.gross_profit))
            operational_profit.append(int(data.operational_profit))
            proceed_profit.append(int(data.proceed_profit))
            net_profit.append(int(data.net_profit))
            construction_overhead.append(int(data.construction_overhead))
            consuming_material.append(int(data.consuming_material))
            production_total_price.append(int(data.production_total_price))

        print(production_fee)

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
            'total_debt': total_debt,
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
