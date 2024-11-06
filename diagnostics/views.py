from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from diagnostics.serializers import AgilityChartSerializer, AssetChartSerializer, BankrupsyChartSerializer, CostChartSerializer, DebtChartSerializer, EquityChartSerializer, FinancialDataSerializer, InventoryChartSerializer, LeverageChartSerializer, LiquidityChartSerializer, ProfitChartSerializer, ProfitibilityChartSerializer, SaleChartSerializer
from .models import FinancialData


class DiagnosticAnalysisViewSet(ModelViewSet):

    permission_classes = [IsAuthenticated]

    serializer_class = FinancialDataSerializer

    CHART_SERIALIZER_MAP = {
        "debt": DebtChartSerializer,
        "asset": AssetChartSerializer,
        "sale": SaleChartSerializer,
        "equity": EquityChartSerializer,
        "bankrupsy": BankrupsyChartSerializer,
        "profitibility": ProfitibilityChartSerializer,
        # dastmozd chart
        "inventory": InventoryChartSerializer,
        "agility": AgilityChartSerializer,
        "liquidity": LiquidityChartSerializer,
        "leverage": LeverageChartSerializer,
        "cost": CostChartSerializer,
        "profit": ProfitChartSerializer,
    }

    def get_serializer_class(self):
        if self.action == "chart":
            chart = self.kwargs.get('slug')

            serializer_class = self.CHART_SERIALIZER_MAP.get(chart)

            if serializer_class is None:
                raise NotFound(
                    detail=f"No serializer found for slug '{chart}'.")

            return serializer_class

        return super().get_serializer_class()

    def get_queryset(self):
        company = self.request.user.company
        print(company)
        print(FinancialData.objects.select_related('financial_asset').prefetch_related(
            'analysis_reports').filter(financial_asset__company=company))
        return FinancialData.objects.select_related('financial_asset').prefetch_related('analysis_reports').filter(financial_asset__company=company)

    @action(detail=False, methods=['get'], url_path='chart/(?P<slug>[^/.]+)', url_name='chart')
    def chart(self, request, slug=None):
        queryset = self.get_queryset()

        if not queryset.exists():
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


# class DiagnosticAnalysisViewSet(ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = FinancialDataSerializer  # Default serializer

#     CHART_SERIALIZER_MAP = {
#         "debt": DebtChartSerializer,
#         "asset": AssetChartSerializer,
#         "sale": SaleChartSerializer,
#         "equity": EquityChartSerializer,
#         "bankrupsy": BankrupsyChartSerializer,
#         "profitibility": ProfitibilityChartSerializer,
#         "inventory": InventoryChartSerializer,
#         "agility": AgilityChartSerializer,
#         "liquidity": LiquidityChartSerializer,
#         "leverage": LeverageChartSerializer,
#         "cost": CostChartSerializer,
#         "profit": ProfitChartSerializer,
#     }

#     def get_serializer_class(self):
#         if self.action == "chart":
#             chart = self.kwargs.get('slug')
#             serializer_class = self.CHART_SERIALIZER_MAP.get(chart)
#             if serializer_class is None:
#                 raise NotFound(
#                     detail=f"No serializer found for slug '{chart}'.")
#             return serializer_class
#         return super().get_serializer_class()

#     def get_queryset(self):
#         # We retrieve and group data by year, organizing by month within each year
#         company = self.request.user.company
#         queryset = FinancialData.objects.select_related('financial_asset').prefetch_related('analysis_reports').filter(
#             financial_asset__company=company
#         )

#         data_by_year = {}
#         for entry in queryset:
#             year = entry.financial_asset.year
#             if year not in data_by_year:
#                 data_by_year[year] = {
#                     'id': entry.id,
#                     'is_monthly': entry.financial_asset.month is not None,
#                     'year': year,
#                     'monthly_data': []
#                 }
#             # Append monthly data for each year
#             monthly_data = {
#                 'month': entry.financial_asset.month,
#                 'current_asset': entry.current_asset,
#                 'non_current_asset': entry.non_current_asset,
#                 'total_asset': entry.total_asset,
#                 "current_debt": entry.current_debt,
#                 "non_current_debt": entry.non_current_debt,
#                 "total_debt": entry.total_debt,
#                 "total_equity": entry.total_equity,
#                 "total_sum_equity_debt": entry.total_sum_equity_debt,
#                 "gross_profit": entry.gross_profit,
#                 "net_sale": entry.net_sale,
#                 "inventory": entry.inventory,
#                 "operational_profit": entry.operational_profit,
#                 "proceed_profit": entry.proceed_profit,
#                 "net_profit": entry.net_profit,
#                 "consuming_material": entry.consuming_material,
#                 "production_fee": entry.production_fee,
#                 "construction_overhead": entry.construction_overhead,
#                 "production_total_price": entry.production_total_price,
#                 "salary_fee": entry.salary_fee,
#                 "salary_production_fee": entry.salary_production_fee,
#                 "usability": entry.usability,
#                 "efficiency": entry.efficiency,
#                 "roa": entry.roa,
#                 "roab": entry.roab,
#                 "roe": entry.roe,
#                 "gross_profit_margin": entry.gross_profit_margin,
#                 "profit_margin_ratio": entry.profit_margin_ratio,
#                 "debt_ratio": entry.debt_ratio,
#                 "capital_ratio": entry.capital_ratio,
#                 "proprietary_ratio": entry.proprietary_ratio,
#                 "equity_per_total_debt_ratio": entry.equity_per_total_debt_ratio,
#                 "equity_per_total_non_current_asset_ratio": entry.equity_per_total_non_current_asset_ratio,
#                 "current_ratio": entry.current_ratio,
#                 "instant_ratio": entry.instant_ratio,
#                 "stock_turnover": entry.stock_turnover,
#                 "altman_bankrupsy_ratio": entry.altman_bankrupsy_ratio,
#             }
#             data_by_year[year]['monthly_data'].append(monthly_data)

#         # Convert dictionary to a list format for the serializer
#         grouped_data = list(data_by_year.values())

#         print(grouped_data)

#         # Convert dictionary to a list format for the serializer
#         return grouped_data

#     @action(detail=False, methods=['get'], url_path='chart/(?P<slug>[^/.]+)', url_name='chart')
#     def chart(self, request, slug=None):
#         queryset = self.get_queryset()

#         if not queryset.exists():
#             return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = self.get_serializer(queryset, many=True)

#         return Response(serializer.data)
