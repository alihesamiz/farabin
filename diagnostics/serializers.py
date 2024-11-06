from rest_framework import serializers
from .models import AnalysisReport, FinancialData


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

    # 'current_asset', 'non_current_asset', 'total_asset',
    #               'current_debt', 'non_current_debt', 'total_debt', 'total_equity',
    #               'total_sum_equity_debt', 'gross_profit', 'net_sale', 'inventory',
    #               'operational_profit', 'proceed_profit', 'net_profit', 'consuming_material',
    #               'production_fee', 'construction_overhead', 'production_total_price',
    #               'salary_fee', 'salary_production_fee', 'usability', 'efficiency', 'roa',
    #               'roab', 'roe', 'gross_profit_margin', 'profit_margin_ratio', 'debt_ratio',
    #               'capital_ratio', 'proprietary_ratio', 'equity_per_total_debt_ratio',
    #               'equity_per_total_non_current_asset_ratio', 'current_ratio', 'instant_ratio',
    #               'stock_turnover', 'altman_bankrupsy_ratio'

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


# class FinancialDataSerializer(serializers.ModelSerializer):
#     is_monthly = serializers.SerializerMethodField()
#     financial_asset = serializers.SerializerMethodField()

#     class Meta:
#         model = FinancialData
#         fields = ['id', 'is_monthly',
#                   'financial_asset', 'current_asset', 'non_current_asset', 'total_asset',
#                   'current_debt', 'non_current_debt', 'total_debt', 'total_equity',
#                   'total_sum_equity_debt', 'gross_profit', 'net_sale', 'inventory',
#                   'operational_profit', 'proceed_profit', 'net_profit', 'consuming_material',
#                   'production_fee', 'construction_overhead', 'production_total_price',
#                   'salary_fee', 'salary_production_fee', 'usability', 'efficiency', 'roa',
#                   'roab', 'roe', 'gross_profit_margin', 'profit_margin_ratio', 'debt_ratio',
#                   'capital_ratio', 'proprietary_ratio', 'equity_per_total_debt_ratio',
#                   'equity_per_total_non_current_asset_ratio', 'current_ratio', 'instant_ratio',
#                   'stock_turnover', 'altman_bankrupsy_ratio',]

#     def get_financial_asset(self, obj):
#         return {"year": obj.financial_asset.year, "month": obj.financial_asset.month if obj.financial_asset.month else "", }

#     def get_is_monthly(self, obj):
#         return True if obj.financial_asset.month else False


# class FinancialDataSerializer(serializers.ModelSerializer):
#     is_monthly = serializers.SerializerMethodField()
#     year = serializers.SerializerMethodField()
#     monthly_data = serializers.SerializerMethodField()

#     class Meta:
#         model = FinancialData
#         fields = ['id', 'is_monthly', 'year', 'monthly_data']

#     def get_year(self, obj):
#         return obj.financial_asset.year

#     def get_is_monthly(self, obj):
#         return True if obj.financial_asset.month else False

#     def get_monthly_data(self, obj):
#         # Modify here if `obj` has related instances for each month
#         return [{
#             "month": obj.financial_asset.month,
#             "current_asset": obj.current_asset,
#             "non_current_asset": obj.non_current_asset,
#             "total_asset": obj.total_asset,
#             "current_debt": obj.current_debt,
#             "non_current_debt": obj.non_current_debt,
#             "total_debt": obj.total_debt,
#             "total_equity": obj.total_equity,
#             "total_sum_equity_debt": obj.total_sum_equity_debt,
#             "gross_profit": obj.gross_profit,
#             "net_sale": obj.net_sale,
#             "inventory": obj.inventory,
#             "operational_profit": obj.operational_profit,
#             "proceed_profit": obj.proceed_profit,
#             "net_profit": obj.net_profit,
#             "consuming_material": obj.consuming_material,
#             "production_fee": obj.production_fee,
#             "construction_overhead": obj.construction_overhead,
#             "production_total_price": obj.production_total_price,
#             "salary_fee": obj.salary_fee,
#             "salary_production_fee": obj.salary_production_fee,
#             "usability": obj.usability,
#             "efficiency": obj.efficiency,
#             "roa": obj.roa,
#             "roab": obj.roab,
#             "roe": obj.roe,
#             "gross_profit_margin": obj.gross_profit_margin,
#             "profit_margin_ratio": obj.profit_margin_ratio,
#             "debt_ratio": obj.debt_ratio,
#             "capital_ratio": obj.capital_ratio,
#             "proprietary_ratio": obj.proprietary_ratio,
#             "equity_per_total_debt_ratio": obj.equity_per_total_debt_ratio,
#             "equity_per_total_non_current_asset_ratio": obj.equity_per_total_non_current_asset_ratio,
#             "current_ratio": obj.current_ratio,
#             "instant_ratio": obj.instant_ratio,
#             "stock_turnover": obj.stock_turnover,
#             "altman_bankrupsy_ratio": obj.altman_bankrupsy_ratio
#         }]

#     def to_representation(self, instance):
#         rep = super().to_representation(instance)
#         # Flatten the year and move monthly data to a nested structure as requested
#         return {
#             "id": rep["id"],
#             "is_monthly": rep["is_monthly"],
#             "year": rep["year"],
#             "monthly_data": rep["monthly_data"]
#         }


class FinancialDataSerializer(serializers.ModelSerializer):
    is_monthly = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    monthly_data = serializers.SerializerMethodField()

    class Meta:
        model = FinancialData
        fields = ['id', 'is_monthly', 'year', 'monthly_data']

    def get_year(self, obj):
        return obj.financial_asset.year

    def get_is_monthly(self, obj):
        # Handle the case when financial_asset or month is None
        return True if obj.financial_asset and obj.financial_asset.month else False

    def get_monthly_data(self, obj):
        # Initialize the list of months (1 through 12)
        months = range(1, 13)  # Months 1 to 12
        monthly_values = {
            "month": [],
            "current_asset": [],
            "non_current_asset": [],
            "total_asset": [],
            "current_debt": [],
            "non_current_debt": [],
            "total_debt": [],
            "total_equity": [],
            "total_sum_equity_debt": [],
            "gross_profit": [],
            "net_sale": [],
            "inventory": [],
            "operational_profit": [],
            "proceed_profit": [],
            "net_profit": [],
            "consuming_material": [],
            "production_fee": [],
            "construction_overhead": [],
            "production_total_price": [],
            "salary_fee": [],
            "salary_production_fee": [],
            "usability": [],
            "efficiency": [],
            "roa": [],
            "roab": [],
            "roe": [],
            "gross_profit_margin": [],
            "profit_margin_ratio": [],
            "debt_ratio": [],
            "capital_ratio": [],
            "proprietary_ratio": [],
            "equity_per_total_debt_ratio": [],
            "equity_per_total_non_current_asset_ratio": [],
            "current_ratio": [],
            "instant_ratio": [],
            "stock_turnover": [],
            "altman_bankrupsy_ratio": [],
        }

        # Prefetch all relevant data for this object
        financial_data = obj.financial_data.filter(month__in=months)
        data_dict = {data.month: data for data in financial_data}

        for month in months:
            # Check if data exists for this month
            data = data_dict.get(month)
            if data:
                # Append actual data if exists
                monthly_values["month"].append(month)
                monthly_values["current_asset"].append(data.current_asset)
                monthly_values["non_current_asset"].append(
                    data.non_current_asset)
                monthly_values["total_asset"].append(data.total_asset)
                monthly_values["current_debt"].append(data.current_debt)
                monthly_values["non_current_debt"].append(
                    data.non_current_debt)
                monthly_values["total_debt"].append(data.total_debt)
                monthly_values["total_equity"].append(data.total_equity)
                monthly_values["total_sum_equity_debt"].append(
                    data.total_sum_equity_debt)
                monthly_values["gross_profit"].append(data.gross_profit)
                monthly_values["net_sale"].append(data.net_sale)
                monthly_values["inventory"].append(data.inventory)
                monthly_values["operational_profit"].append(
                    data.operational_profit)
                monthly_values["proceed_profit"].append(data.proceed_profit)
                monthly_values["net_profit"].append(data.net_profit)
                monthly_values["consuming_material"].append(
                    data.consuming_material)
                monthly_values["production_fee"].append(data.production_fee)
                monthly_values["construction_overhead"].append(
                    data.construction_overhead)
                monthly_values["production_total_price"].append(
                    data.production_total_price)
                monthly_values["salary_fee"].append(data.salary_fee)
                monthly_values["salary_production_fee"].append(
                    data.salary_production_fee)
                monthly_values["usability"].append(data.usability)
                monthly_values["efficiency"].append(data.efficiency)
                monthly_values["roa"].append(data.roa)
                monthly_values["roab"].append(data.roab)
                monthly_values["roe"].append(data.roe)
                monthly_values["gross_profit_margin"].append(
                    data.gross_profit_margin)
                monthly_values["profit_margin_ratio"].append(
                    data.profit_margin_ratio)
                monthly_values["debt_ratio"].append(data.debt_ratio)
                monthly_values["capital_ratio"].append(data.capital_ratio)
                monthly_values["proprietary_ratio"].append(
                    data.proprietary_ratio)
                monthly_values["equity_per_total_debt_ratio"].append(
                    data.equity_per_total_debt_ratio)
                monthly_values["equity_per_total_non_current_asset_ratio"].append(
                    data.equity_per_total_non_current_asset_ratio)
                monthly_values["current_ratio"].append(data.current_ratio)
                monthly_values["instant_ratio"].append(data.instant_ratio)
                monthly_values["stock_turnover"].append(data.stock_turnover)
                monthly_values["altman_bankrupsy_ratio"].append(
                    data.altman_bankrupsy_ratio)
            else:
                # If no data for the month, append None for each field
                monthly_values["month"].append(month)
                for key in monthly_values.keys():
                    if key != "month":
                        monthly_values[key].append(None)

        return monthly_values

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # Flatten the year and move monthly data to a nested structure as requested
        return {
            "id": rep["id"],
            "is_monthly": rep["is_monthly"],
            "year": rep["year"],
            "monthly_data": rep["monthly_data"]
        }
