from rest_framework import serializers


from management.models import HumanResource, PersonelInformation, OrganizationChartBase
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


class PersonelInformationSerializer(serializers.ModelSerializer):

    human_resource_id = serializers.PrimaryKeyRelatedField(
        source="human_resource", read_only=True
    )

    node_relation = serializers.SerializerMethodField(
        method_name="get_relation")

    class Meta:
        model = PersonelInformation
        fields = ["id", "human_resource_id", "name", "position",
                  "reports_to", "obligations", "node_relation"]
        read_only_fields = ["id", "human_resource_id"]

    def get_relation(self, obj):
        return f"{obj.id}-{obj.reports_to}"


class PersonelInformationCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = PersonelInformation
        fields = ["human_resource", "name",
                  "position", "reports_to", "obligations"]


class PersonelInformationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonelInformation
        fields = ["name", "position", "reports_to", "obligations"]
        extra_kwargs = {
            "name": {"required": False},
            "position": {"required": False},
            "reports_to": {"required": False},
            "obligations": {"required": False},
        }


class OrganizationChartFileSerializer(serializers.ModelSerializer):
    position_excel_url = serializers.FileField(
        source="position_excel", read_only=True)

    class Meta:
        model = OrganizationChartBase
        fields = ["id", "position_excel_url"]


class ChartNodeSerializer(serializers.ModelSerializer):
    reports_to = serializers.SerializerMethodField()

    class Meta:
        model = PersonelInformation
        fields = ['id', 'name', 'position', 'reports_to', "obligations"]

    def get_reports_to(self, obj):
        return obj.reports_to.id if obj.reports_to else None
