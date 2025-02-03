from rest_framework import serializers


from management.models import HumanResource
from company.models import CompanyProfile


class HumanResourceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanResource
        fields = ['excel_file']  # , 'company']

    def validate_company(self, value):
        if HumanResource.objects.filter(company=value).exists():
            raise serializers.ValidationError(
                "Each company can only have one Human Resource record.")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        company = CompanyProfile.objects.get(user=user)
        validated_data['company'] = company

        return super().create(validated_data)


class HumanResourceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanResource
        fields = ['excel_file']
        extra_kwargs = {'excel_file': {'required': False}}


class HumanResourceSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = HumanResource
        fields = ['id', 'excel_file', 'company',
                  'company_name', 'create_at', 'updated_at']
        read_only_fields = ['id', 'create_at', 'updated_at']
