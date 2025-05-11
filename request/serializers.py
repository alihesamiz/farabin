from rest_framework import serializers

from request.models import BaseRequest, FinanceRequest, ManagementRequest

from finance.serializers import (
    SimpleTaxDeclarationSerializer,
    SimpleBalanceReportSerializer,
)
from management.serializers import HumanResourceSerializer


class BaseRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseRequest
        fields = ["id", "status", "subject", "created_at", "updated_at"]

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
        fields = BaseRequestSerializer.Meta.fields + ["tax_record", "balance_record"]


class ManagementRequestSerializer(BaseRequestSerializer):
    human_resource_record = HumanResourceSerializer()

    class Meta(BaseRequestSerializer.Meta):
        model = ManagementRequest
        fields = BaseRequestSerializer.Meta.fields + ["human_resource_record"]
