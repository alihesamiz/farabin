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

        return FinancialData.objects.select_related('financial_asset').prefetch_related('analysis_reports').filter(financial_asset__company=company)

    @action(detail=False, methods=['get'], url_path='chart/(?P<slug>[^/.]+)', url_name='chart')
    def chart(self, request, slug=None):
        queryset = self.get_queryset()
        
        if not queryset.exists():
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        
        return Response(serializer.data)
