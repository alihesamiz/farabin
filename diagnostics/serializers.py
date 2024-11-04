from rest_framework import serializers
from .models import AnalysisReport, FinancialData, SoldProductFee, ProfitLossStatement, BalanceReport, AccountTurnOver, FinancialAsset


class FinancialAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialAsset
        fields = '__all__'


class BaseChartSerializer(serializers.Serializer):
    financial_asset = serializers.SerializerMethodField()
    report = serializers.SerializerMethodField()

    def __init__(self, *args, chart_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.chart_name = chart_name

    def get_financial_asset(self, obj):
        return {
            "year": obj.financial_asset.year,
            "month": obj.financial_asset.month if obj.financial_asset.month else '-'
        }

    def get_report(self, obj):
        # Filter reports to only include those corresponding to the specified chart
        reports = obj.analysis_reports.filter(chart_name=self.chart_name)
        return AnalysisReportSerializer(reports, many=True).data


class AssetChartSerializer(BaseChartSerializer):
    current_asset = serializers.DecimalField(max_digits=10, decimal_places=2)
    non_current_asset = serializers.DecimalField(
        max_digits=10, decimal_places=2)
    total_asset = serializers.DecimalField(max_digits=10, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.ASSET_CHART, **kwargs)


class DebtChartSerializer(BaseChartSerializer):
    current_debt = serializers.DecimalField(max_digits=10, decimal_places=2)
    non_current_debt = serializers.DecimalField(
        max_digits=10, decimal_places=2)
    total_debt = serializers.DecimalField(max_digits=10, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.DEBT_CHART, **kwargs)

# Make sure you have a proper serializer for AnalysisReport defined


class AnalysisReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisReport
        fields = ['chart_name', 'text']


class FinancialDataSerializer(serializers.ModelSerializer):
    financial_asset = serializers.SerializerMethodField()
    # charts = AnalysisReportSerializer(many=True, source='analysis_reports')

    class Meta:
        model = FinancialData
        fields = ['id',
                  'financial_asset', 'current_asset', 'non_current_asset', 'total_asset',
                  'current_debt', 'non_current_debt', 'total_debt', 'total_equity',
                  'total_sum_equity_debt', 'gross_profit', 'net_sale', 'inventory',
                  'operational_profit', 'proceed_profit', 'net_profit', 'consuming_material',
                  'production_fee', 'construction_overhead', 'production_total_price',
                  'salary_fee', 'salary_production_fee', 'usability', 'efficiency', 'roa',
                  'roab', 'roe', 'gross_profit_margin', 'profit_margin_ratio', 'debt_ratio',
                  'capital_ratio', 'proprietary_ratio', 'equity_per_total_debt_ratio',
                  'equity_per_total_non_current_asset_ratio', 'current_ratio', 'instant_ratio',
                  'stock_turnover', 'altman_bankrupsy_ratio',]  # 'charts']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Precompute the financial asset data once and store it
        self.financial_asset_info = {
            "year": self.instance.financial_asset.year,
            "month": self.instance.financial_asset.month if self.instance.financial_asset.month else '-'
        } if self.instance else None

    def get_financial_asset(self, obj):
        # Simply return the precomputed value
        return self.financial_asset_info
