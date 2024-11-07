from django.db.models import Max
from django.db.models import Prefetch
from collections import defaultdict
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.decorators import action
from .serializers import (AgilityChartSerializer, AssetChartSerializer, BankrupsyChartSerializer, CostChartSerializer, DebtChartSerializer, EquityChartSerializer, FinancialAssetSerializer, FinancialDataSerializer,
                          InventoryChartSerializer, LeverageChartSerializer, LiquidityChartSerializer, FinancialDataSerializer, MonthDataSerializer, MonthlyFinancialDataSerializer, ProfitChartSerializer, ProfitibilityChartSerializer, SaleChartSerializer, YearlyFinanceDataSerializer)
from .models import FinancialAsset, FinancialData


# class DiagnosticAnalysisViewSet(ModelViewSet):

#     permission_classes = [IsAuthenticated]

#     serializer_class = FinancialAssetSerializer

#     CHART_SERIALIZER_MAP = {
#         "debt": DebtChartSerializer,
#         "asset": AssetChartSerializer,
#         "sale": SaleChartSerializer,
#         "equity": EquityChartSerializer,
#         "bankrupsy": BankrupsyChartSerializer,
#         "profitibility": ProfitibilityChartSerializer,
#         # dastmozd chart
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

#         if self.action == 'year':
#             pass
#         elif self.action == 'month':
#             pass

#         return super().get_serializer_class()

#     def get_queryset(self):
#         company = self.request.user.company
#         return FinancialData.objects.select_related('financial_asset').prefetch_related('analysis_reports').filter(financial_asset__company=company).filter(financial_asset__is_tax_record=True)

#     @action(detail=False, methods=['get'], url_path='chart/(?P<slug>[^/.]+)', url_name='chart')
#     def chart(self, request, slug=None):
#         queryset = self.get_queryset()

#         if not queryset.exists():
#             return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

#         serializer = self.get_serializer(queryset, many=True)

#         return Response(serializer.data)

#     @action(detail=False, methods=['get'], url_path='year/', url_name='year')
#     def year(self, request):
#         queryset = self.get_queryset().filter(financial_asset__is_tax_record=True)

#         serializer = self.get_serializer(queryset, many=True)

#         return Response(serializer.data)

#     @action(detail=False, methods=['get'], url_path='month/', url_name='month')
#     def year(self, request):
#         queryset = self.get_queryset().filter(financial_asset__is_tax_record=False)

#         serializer = self.get_serializer(queryset, many=True)

#         return Response(serializer.data)


# class DiagnosticAnalysisViewSet(ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = FinancialAssetSerializer

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
#         # elif self.action == 'year':
#         #     return YearChartSerializer  # Define as needed
#         # elif self.action == 'month':
#         #     return MonthChartSerializer  # Define as needed
#         return super().get_serializer_class()

#     def get_queryset(self):
#         company = self.request.user.company
#         return FinancialData.objects.select_related('financial_asset').prefetch_related('analysis_reports').filter(
#             financial_asset__company=company, financial_asset__is_tax_record=True)

#     @action(detail=False, methods=['get'], url_path='chart/(?P<slug>[^/.]+)', url_name='chart')
#     def chart(self, request, slug=None):
#         queryset = self.get_queryset()
#         if queryset:
#             return Response({'detail': f"No data found for '{slug}' chart."}, status=status.HTTP_404_NOT_FOUND)
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

# @action(detail=False, methods=['get'], url_path='year/', url_name='year')
# def year(self, request):
#     queryset = self.get_queryset().filter(financial_asset__is_tax_record=True)
#     if not queryset.exists():
#         return Response({'detail': 'No yearly data found.'}, status=status.HTTP_404_NOT_FOUND)
#     serializer = self.get_serializer(queryset, many=True)
#     return Response(serializer.data)

# @action(detail=False, methods=['get'], url_path='month/', url_name='month')
# def month(self, request):
#     queryset = self.get_queryset().filter(financial_asset__is_tax_record=False)
#     if not queryset.exists():
#         return Response({'detail': 'No monthly data found.'}, status=status.HTTP_404_NOT_FOUND)
#     serializer = self.get_serializer(queryset, many=True)
#     return Response(serializer.data)


# class DiagnosticAnalysisViewSet(ModelViewSet):

#     CHART_SERIALIZER_MAP = {
#         "debt": DebtChartSerializer,
#         "asset": AssetChartSerializer,
#         "sale": SaleChartSerializer,
#         "equity": EquityChartSerializer,
#         "bankrupsy": BankrupsyChartSerializer,
#         "profitibility": ProfitibilityChartSerializer,
#         # dastmozd chart
#         "inventory": InventoryChartSerializer,
#         "agility": AgilityChartSerializer,
#         "liquidity": LiquidityChartSerializer,
#         "leverage": LeverageChartSerializer,
#         "cost": CostChartSerializer,
#         "profit": ProfitChartSerializer,
#     }

#     permission_classes = [IsAuthenticated]

#     serializer_class = FinancialDataSerializer

#     def get_serializer_class(self):
#         print(self.action)

#         if self.action == "month":

#             return YearlyFinanceDataSerializer
#         if self.action == "chart":
#             chart = self.kwargs.get('slug')
#             print('chart')
#             serializer_class = self.CHART_SERIALIZER_MAP.get(chart)
#             if serializer_class is None:
#                 raise NotFound(
#                     detail=f"No serializer found for slug '{chart}'.")
#             return serializer_class

#         return super().get_serializer_class()

#     def get_queryset(self):
#         company = self.request.user.company
#         financial_data = FinancialData.objects.select_related('financial_asset').filter(
#             financial_asset__company=company, financial_asset__is_tax_record=True, is_published=True).all()
#         if financial_data.exists():
#             return financial_data
#         else:
#             return []

#     @action(detail=False, methods=['get'], url_path='chart/(?P<slug>[^/.]+)', url_name='chart')
#     def chart(self, request, slug=None):
#         queryset = self.get_queryset()
#         if not queryset:
#             return Response({'detail': f"No data found for '{slug}' chart."}, status=status.HTTP_404_NOT_FOUND)
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

#     @action(detail=False, methods=['get'], url_path='month', url_name='month')
#     def month(self, request):
#         company = request.user.company

#         data_by_year = {}
#         queryset = FinancialData.objects.select_related('financial_asset').filter(
#             financial_asset__company=company,
#             financial_asset__is_tax_record=False,
#             is_published=True
#         )

#         for data in queryset:
#             year = data.financial_asset.year
#             if year not in data_by_year:
#                 data_by_year[year] = []
#             data_by_year[year].append(data)

#         # Serialize data
#         result = [
#             {
#                 'year': year,
#                 'months': MonthDataSerializer(month_data, many=True).data
#             }
#             for year, month_data in data_by_year.items()
#         ]
#         if not result:
#             return Response({'detail': 'No monthly data found.'}, status=status.HTTP_404_NOT_FOUND)

#         return Response(result)


from itertools import groupby
from operator import attrgetter
from .models import FinancialData, FinancialAsset


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
        elif self.action == "chart":
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

        # Serialize data
        result = [
            {
                'year': year,
                'months': MonthDataSerializer(month_data, many=True).data
            }
            for year, month_data in data_by_year.items()
        ]

        return Response(result)
