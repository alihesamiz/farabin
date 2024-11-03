from rest_framework import serializers
from .models import AnalysisReport, FinancialData, SoldProductFee, ProfitLossStatement, BalanceReport, AccountTurnOver, FinancialAsset


class SoldProductFeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SoldProductFee
        fields = '__all__'  # List specific fields if you need to limit the fields


class ProfitLossStatementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfitLossStatement
        fields = '__all__'


class BalanceReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = BalanceReport
        fields = '__all__'


class AccountTurnOverSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountTurnOver
        fields = '__all__'


class FinancialAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialAsset
        fields = '__all__'


# class FinancialAssetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FinancialAsset
#         fields = ['year']  # Include other fields from FinancialAsset if needed


# class FinancialDataSerializer(serializers.ModelSerializer):
#     financial_asset = FinancialAssetSerializer()  # Use the nested serializer

#     class Meta:
#         model = FinancialData
#         fields = [
#             'financial_asset', 'current_asset', 'non_current_asset', 'total_asset',
#             'current_debt', 'non_current_debt', 'total_debt', 'total_equity',
#             'total_sum_equity_debt', 'gross_profit', 'net_sale', 'inventory',
#             'operational_profit', 'proceed_profit', 'net_profit', 'consuming_material',
#             'production_fee', 'construction_overhead', 'production_total_price',
#             'salary_fee', 'salary_production_fee', 'usability', 'efficiency',
#             'roa', 'roab', 'roe', 'gross_profit_margin', 'profit_margin_ratio',
#             'debt_ratio', 'capital_ratio', 'proprietary_ratio',
#             'equity_per_total_debt_ratio', 'equity_per_total_non_current_asset_ratio',
#             'current_ratio', 'instant_ratio', 'stock_turnover',
#             'altman_bankrupsy_ratio'
#         ]


# class AnalysisReportSerializer(serializers.ModelSerializer):

#     calculated_data = FinancialDataSerializer()

#     class Meta:
#         model = AnalysisReport
#         fields = [
#             'calculated_data', 'chart_name', 'text'
#         ]


# class AnalysisReportSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AnalysisReport
#         fields = ['id', 'chart_name', 'text']


class FinancialDataSerializer(serializers.ModelSerializer):
    financial_asset = serializers.SerializerMethodField()
    # charts = AnalysisReportSerializer(many=True, source='analysis_reports')

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
            'stock_turnover', 'altman_bankrupsy_ratio',]  # 'charts']

    def get_financial_asset(self, obj):
        return {"year": obj.financial_asset.year}
