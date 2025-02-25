
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from finance.models import AnalysisReport, FinanceExcelFile, FinancialAsset, FinancialData, BalanceReportFile, TaxDeclarationFile
from company.models import CompanyProfile


class BalanceReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceReportFile
        fields = ['year', 'month', 'balance_report_file',
                  'profit_loss_file', 'sold_product_file', 'account_turnover_file', 'is_saved', 'is_sent']

    def create(self, validated_data):
        user = self.context['request'].user
        company = CompanyProfile.objects.get(user=user)
        validated_data['company'] = company

        year = validated_data.get('year')
        month = validated_data.get('month')
        existing_report = BalanceReportFile.objects.filter(
            company=company, year=year, month=month).first()

        if existing_report:
            raise ValidationError(
                {"error": "This months' file already exists"})

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Handle file updates
        for field in ['balance_report_file', 'profit_loss_file', 'sold_product_file', 'account_turnover_file']:
            new_file = validated_data.get(field)
            if new_file and getattr(instance, field) != new_file:
                # Delete old file before saving the new one
                old_file = getattr(instance, field)
                if old_file:
                    old_file.delete()  # Delete the old file

        return super().update(instance, validated_data)


class BalanceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceReportFile
        fields = ['id', 'year', 'month', 'balance_report_file',
                  'profit_loss_file', 'sold_product_file', 'account_turnover_file', 'is_saved', 'is_sent']


class SimpleBalanceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceReportFile
        fields = ['id', 'year', 'month',]


class TaxDeclarationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxDeclarationFile
        fields = ['year', 'tax_file']

    def create(self, validated_data):
        user = self.context['request'].user
        company = CompanyProfile.objects.get(user=user)
        validated_data['company'] = company

        year = validated_data.get('year')
        existing_report = TaxDeclarationFile.objects.filter(
            company=company, year=year).first()

        if existing_report:
            raise ValidationError({"error": "This years' file already exists"})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Handle file update
        tax_file = validated_data.get('tax_file', None)
        if tax_file and instance.tax_file != tax_file:
            # Optionally, you can handle file replacement here too
            old_file = instance.tax_file
            if old_file:
                old_file.delete()  # Delete the old file before saving the new one

        return super().update(instance, validated_data)


class TaxDeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxDeclarationFile
        fields = ['id',  'year', 'tax_file', 'is_saved', 'is_sent']


class SimpleTaxDeclarationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxDeclarationFile
        fields = ['id',  'year']


class FinanceExcelFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceExcelFile
        fields = ['id', 'company', 'finance_excel_file', 'is_saved', 'is_sent']


class BaseChartSerializer(serializers.Serializer):
    financial_asset = serializers.SerializerMethodField()
    report = serializers.SerializerMethodField()

    def __init__(self, *args, chart_name=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.chart_name = chart_name

    def get_financial_asset(self, obj):
        # Start with the year always being included
        financial_asset_data = {"year": obj.financial_asset.year}

        # Only add the 'month' if it exists
        if obj.financial_asset.month:
            financial_asset_data["month"] = obj.financial_asset.month

        return financial_asset_data

    def get_report(self, obj):
        # Filter reports to only include those corresponding to the specified chart
        reports = obj.analysis_reports.filter(chart_name=self.chart_name)
        return AnalysisReportSerializer(reports, many=True).data


class AssetChartSerializer(BaseChartSerializer):
    current_asset = serializers.DecimalField(max_digits=20, decimal_places=2)
    non_current_asset = serializers.DecimalField(
        max_digits=20, decimal_places=2)
    total_asset = serializers.DecimalField(max_digits=20, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.ASSET_CHART, **kwargs)


class SaleChartSerializer(BaseChartSerializer):
    net_sale = serializers.DecimalField(max_digits=20, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.SALE_CHART, **kwargs)


class EquityChartSerializer(BaseChartSerializer):
    total_equity = serializers.DecimalField(max_digits=20, decimal_places=2)

    total_debt = serializers.DecimalField(max_digits=20, decimal_places=2)

    total_sum_equity_debt = serializers.DecimalField(
        max_digits=20, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.DEBT_CHART, **kwargs)


class BankrupsyChartSerializer(BaseChartSerializer):

    altman_bankrupsy_ratio = serializers.DecimalField(
        max_digits=5, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.BANKRUPSY_CHART, **kwargs)


class ProfitibilityChartSerializer(BaseChartSerializer):
    roa = serializers.DecimalField(max_digits=20, decimal_places=2)

    roab = serializers.DecimalField(
        max_digits=20, decimal_places=2)

    usability = serializers.DecimalField(max_digits=20, decimal_places=2)

    efficiency = serializers.DecimalField(max_digits=20, decimal_places=2)

    gross_profit_margin = serializers.DecimalField(
        max_digits=20, decimal_places=2)

    profit_margin_ratio = serializers.DecimalField(
        max_digits=20, decimal_places=2)

    roe = serializers.DecimalField(max_digits=20, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.PROFITIBILITY_CHART, **kwargs)


class InventoryChartSerializer(BaseChartSerializer):

    inventory_average = serializers.DecimalField(
        max_digits=20, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.INVENTORY_CHART, **kwargs)


class AgilityChartSerializer(BaseChartSerializer):
    instant_ratio = serializers.DecimalField(max_digits=20, decimal_places=2)

    stock_turnover = serializers.DecimalField(
        max_digits=20, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.AGILITY_CHART, **kwargs)


class DebtChartSerializer(BaseChartSerializer):
    current_debt = serializers.DecimalField(max_digits=20, decimal_places=2)

    non_current_debt = serializers.DecimalField(
        max_digits=20, decimal_places=2)

    total_debt = serializers.DecimalField(max_digits=20, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.DEBT_CHART, **kwargs)


class SalaryChartSerializer(BaseChartSerializer):

    production_total_price = serializers.DecimalField(
        max_digits=20, decimal_places=2)
    salary_fee = serializers.DecimalField(max_digits=20, decimal_places=2)
    salary_production_fee = serializers.DecimalField(
        max_digits=20, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.SALARY_CHART, **kwargs)


class LeverageChartSerializer(BaseChartSerializer):

    debt_ratio = serializers.DecimalField(max_digits=20, decimal_places=2)

    capital_ratio = serializers.DecimalField(max_digits=20, decimal_places=2)

    proprietary_ratio = serializers.DecimalField(
        max_digits=20, decimal_places=2)

    equity_per_total_debt_ratio = serializers.DecimalField(
        max_digits=20, decimal_places=2)

    equity_per_total_non_current_asset_ratio = serializers.DecimalField(
        max_digits=20, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.LEVERAGE_CHART, **kwargs)


class LiquidityChartSerializer(BaseChartSerializer):

    current_ratio = serializers.DecimalField(max_digits=20, decimal_places=2)

    instant_ratio = serializers.DecimalField(
        max_digits=20, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.LIQUIDITY_CHART, **kwargs)


class CostChartSerializer(BaseChartSerializer):

    consuming_material = serializers.DecimalField(
        max_digits=20, decimal_places=2)

    production_fee = serializers.DecimalField(
        max_digits=20, decimal_places=2)

    construction_overhead = serializers.DecimalField(
        max_digits=20, decimal_places=2)

    production_total_price = serializers.DecimalField(
        max_digits=20, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.COST_CHART, **kwargs)


class ProfitChartSerializer(BaseChartSerializer):
    gross_profit = serializers.DecimalField(max_digits=20, decimal_places=2)

    net_sale = serializers.DecimalField(max_digits=20, decimal_places=2)

    operational_profit = serializers.DecimalField(
        max_digits=20, decimal_places=2)

    proceed_profit = serializers.DecimalField(max_digits=20, decimal_places=2)

    net_profit = serializers.DecimalField(
        max_digits=20, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, chart_name=AnalysisReport.PROFIT_CHART, **kwargs)


class AnalysisReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisReport
        fields = ['chart_name', 'text', 'created_at', 'updated_at']


class AnalysisReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisReport
        fields = ['chart_name', 'text', 'created_at', 'updated_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Limit the 'text' field to 20 characters
        representation['text'] = instance.text[:15]
        return representation


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
            'total_sum_equity_debt', 'gross_profit', 'net_sale', 'inventory_average',
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
            'inventory_average',
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
            'inventory_average', 'operational_profit', 'proceed_profit', 'net_profit',
            'consuming_material', 'production_fee', 'construction_overhead', 'production_total_price',
            'salary_fee', 'salary_production_fee', 'usability', 'efficiency', 'roa', 'roab', 'roe',
            'gross_profit_margin', 'profit_margin_ratio', 'debt_ratio', 'capital_ratio',
            'proprietary_ratio', 'equity_per_total_debt_ratio', 'equity_per_total_non_current_asset_ratio',
            'current_ratio', 'instant_ratio', 'stock_turnover', 'altman_bankrupsy_ratio'
        ]


class YearlyFinanceDataSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    months = serializers.ListField(child=MonthDataSerializer())
