from django.shortcuts import render
from .models import AnalysisReport
from itertools import groupby
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from .serializers import (AgilityChartSerializer, AssetChartSerializer, BankrupsyChartSerializer, CostChartSerializer, DebtChartSerializer, EquityChartSerializer, FinancialAssetSerializer, FinancialDataSerializer,
                          InventoryChartSerializer, LeverageChartSerializer, LiquidityChartSerializer, FinancialDataSerializer, MonthDataSerializer, MonthlyFinancialDataSerializer, ProfitChartSerializer, ProfitibilityChartSerializer, SaleChartSerializer, YearlyFinanceDataSerializer)
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


def chart_view(request):
    pass