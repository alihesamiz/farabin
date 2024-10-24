from rest_framework import serializers
from .models import SoldProductFee, ProfitLossStatement, BalanceReport, AccountTurnOver, FinancialAsset


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
