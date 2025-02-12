from rest_framework import serializers

from request.models import BaseRequest, FinanceRequest

from finance.serializers import SimpleTaxDeclarationSerializer, SimpleBalanceReportSerializer


class BaseRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseRequest
        fields = ['id', 'status', 'subject', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        # Custom update logic if needed
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class FinanceRequestSerializer(BaseRequestSerializer):
    tax_record = SimpleTaxDeclarationSerializer()
    balance_record = SimpleBalanceReportSerializer()

    class Meta(BaseRequestSerializer.Meta):
        model = FinanceRequest
        fields = BaseRequestSerializer.Meta.fields + \
            ['tax_record', 'balance_record']


class ManagementRequestSerializer(BaseRequestSerializer):
    tax_record = SimpleTaxDeclarationSerializer()
    balance_record = SimpleBalanceReportSerializer()

    class Meta(BaseRequestSerializer.Meta):
        model = FinanceRequest
        fields = BaseRequestSerializer.Meta.fields + \
            ['tax_record', 'balance_record']
