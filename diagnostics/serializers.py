from rest_framework import serializers
from .models import AnalysisReport, FinancialAsset, FinancialData


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


class SaleChartSerializer(BaseChartSerializer):
    net_sale = serializers.DecimalField(max_digits=20, decimal_places=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.SALE_CHART, **kwargs)


class EquityChartSerializer(BaseChartSerializer):
    total_equity = serializers.DecimalField(max_digits=20, decimal_places=0)

    total_debt = serializers.DecimalField(max_digits=20, decimal_places=0)

    total_sum_equity_debt = serializers.DecimalField(
        max_digits=20, decimal_places=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.DEBT_CHART, **kwargs)


class BankrupsyChartSerializer(BaseChartSerializer):

    altman_bankrupsy_ratio = serializers.DecimalField(
        max_digits=5, decimal_places=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.BANKRUPSY_CHART, **kwargs)


class ProfitibilityChartSerializer(BaseChartSerializer):
    roa = serializers.DecimalField(max_digits=20, decimal_places=0)

    roab = serializers.DecimalField(
        max_digits=20, decimal_places=0)

    usability = serializers.DecimalField(max_digits=20, decimal_places=0)

    efficiency = serializers.DecimalField(max_digits=20, decimal_places=0)

    gross_profit_margin = serializers.DecimalField(
        max_digits=20, decimal_places=0)

    profit_margin_ratio = serializers.DecimalField(
        max_digits=20, decimal_places=0)

    roe = serializers.DecimalField(max_digits=20, decimal_places=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.PROFITIBILITY_CHART, **kwargs)


class InventoryChartSerializer(BaseChartSerializer):

    inventory = serializers.DecimalField(max_digits=20, decimal_places=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.INVENTORY_CHART, **kwargs)


class AgilityChartSerializer(BaseChartSerializer):
    instant_ratio = serializers.DecimalField(max_digits=20, decimal_places=0)

    stock_turnover = serializers.DecimalField(
        max_digits=20, decimal_places=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.AGILITY_CHART, **kwargs)


class DebtChartSerializer(BaseChartSerializer):
    current_debt = serializers.DecimalField(max_digits=10, decimal_places=2)

    non_current_debt = serializers.DecimalField(
        max_digits=10, decimal_places=2)

    total_debt = serializers.DecimalField(max_digits=10, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.DEBT_CHART, **kwargs)


class LiquidityChartSerializer(BaseChartSerializer):

    current_ratio = serializers.DecimalField(max_digits=20, decimal_places=0)

    instant_ratio = serializers.DecimalField(
        max_digits=20, decimal_places=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.LIQUIDITY_CHART, **kwargs)


class LeverageChartSerializer(BaseChartSerializer):

    debt_ratio = serializers.DecimalField(max_digits=20, decimal_places=0)

    capital_ratio = serializers.DecimalField(max_digits=20, decimal_places=0)

    proprietary_ratio = serializers.DecimalField(
        max_digits=20, decimal_places=0)

    equity_per_total_debt_ratio = serializers.DecimalField(
        max_digits=20, decimal_places=0)

    equity_per_total_non_current_asset_ratio = serializers.DecimalField(
        max_digits=20, decimal_places=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.LEVERAGE_CHART, **kwargs)


class LiquidityChartSerializer(BaseChartSerializer):

    current_ratio = serializers.DecimalField(max_digits=20, decimal_places=0)

    instant_ratio = serializers.DecimalField(
        max_digits=20, decimal_places=0)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.LIQUIDITY_CHART, **kwargs)


class CostChartSerializer(BaseChartSerializer):

    consuming_material = serializers.DecimalField(
        max_digits=20, decimal_places=0)

    production_fee = serializers.DecimalField(
        max_digits=20, decimal_places=0)

    construction_overhead = serializers.DecimalField(
        max_digits=20, decimal_places=0)

    production_total_price = serializers.DecimalField(
        max_digits=20, decimal_places=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.COST_CHART, **kwargs)


class ProfitChartSerializer(BaseChartSerializer):
    gross_profit = serializers.DecimalField(max_digits=20, decimal_places=0)

    net_sale = serializers.DecimalField(max_digits=20, decimal_places=0)

    operational_profit = serializers.DecimalField(
        max_digits=20, decimal_places=0)

    proceed_profit = serializers.DecimalField(max_digits=20, decimal_places=0)

    net_profit = serializers.DecimalField(
        max_digits=20, decimal_places=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.PROFIT_CHART, **kwargs)


class AnalysisReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisReport
        fields = ['chart_name', 'text']


class FinancialAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialAsset
        fields = ['year', 'month']


class FinancialDataSerializer(serializers.ModelSerializer):
    financial_asset = FinancialAssetSerializer(read_only=True)

    class Meta:
        model = FinancialData
        fields = [
            'financial_asset', 'current_asset', 'non_current_asset', 'total_asset',
            'current_debt', 'non_current_debt', 'total_debt', 'total_equity',
            'total_sum_equity_debt', 'gross_profit', 'net_sale', 'inventory',
            'operational_profit', 'proceed_profit', 'net_profit', 'consuming_material',
            'production_fee', 'construction_overhead', 'production_total_price',
            'salary_fee', 'salary_production_fee', 'usability', 'efficiency', 'roa',
            'roab', 'roe', 'gross_profit_margin', 'profit_margin_ratio', 'debt_ratio',
            'capital_ratio', 'proprietary_ratio', 'equity_per_total_debt_ratio',
            'equity_per_total_non_current_asset_ratio', 'current_ratio', 'instant_ratio',
            'stock_turnover', 'altman_bankrupsy_ratio'
        ]

    def get_financial_asset(self, instance):
        return {"year": instance.calculated_data.year, "month": instance.financial_asset.month if instance.financial_asset.month else ""}


class MonthlyFinancialDataSerializer(serializers.ModelSerializer):
    financial_asset = FinancialAssetSerializer(read_only=True)

    class Meta:
        model = FinancialData
        fields = [
            'financial_asset',
            'current_asset',
            'non_current_asset',
            'total_asset',
            'current_debt',
            'non_current_debt',
            'total_debt',
            'total_equity',
            'total_sum_equity_debt',
            'gross_profit',
            'net_sale',
            'inventory',
            'operational_profit',
            'proceed_profit',
            'net_profit',
            'consuming_material',
            'production_fee',
            'construction_overhead',
            'production_total_price',
            'salary_fee',
            'salary_production_fee',
            'usability',
            'efficiency',
            'roa',
            'roab',
            'roe',
            'gross_profit_margin',
            'profit_margin_ratio',
            'debt_ratio',
            'capital_ratio',
            'proprietary_ratio',
            'equity_per_total_debt_ratio',
            'equity_per_total_non_current_asset_ratio',
            'current_ratio',
            'instant_ratio',
            'stock_turnover',
            'altman_bankrupsy_ratio'
        ]

    def get_financial_asset(self, instance):
        return {"year": instance.calculated_data.year, "month": instance.financial_asset.month if instance.financial_asset.month else ""}


class MonthDataSerializer(serializers.ModelSerializer):
    month = serializers.IntegerField(source="financial_asset.month")

    class Meta:
        model = FinancialData
        fields = [
            'month', 'current_asset', 'non_current_asset', 'total_asset', 'current_debt',
            'non_current_debt', 'total_debt', 'total_equity', 'gross_profit', 'net_sale',
            'inventory', 'operational_profit', 'proceed_profit', 'net_profit',
            'consuming_material', 'production_fee', 'construction_overhead', 'production_total_price',
            'salary_fee', 'salary_production_fee', 'usability', 'efficiency', 'roa', 'roab', 'roe',
            'gross_profit_margin', 'profit_margin_ratio', 'debt_ratio', 'capital_ratio',
            'proprietary_ratio', 'equity_per_total_debt_ratio', 'equity_per_total_non_current_asset_ratio',
            'current_ratio', 'instant_ratio', 'stock_turnover', 'altman_bankrupsy_ratio'
        ]


class YearlyFinanceDataSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    months = serializers.ListField(child=MonthDataSerializer())
