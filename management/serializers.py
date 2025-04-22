from rest_framework import serializers


from management.models import HumanResource, PersonelInformation, OrganizationChartBase, SWOTMatrix, SWOTOpportunityOption, SWOTStrengthOption, SWOTThreatOption, SWOTWeaknessOption
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

    reports_relation = serializers.SerializerMethodField()

    coops_relation = serializers.SerializerMethodField()

    class Meta:
        model = PersonelInformation
        fields = ["id", "human_resource_id", "name", "position",
                  "reports_to", "cooperates_with", "obligations", "reports_relation", "coops_relation"]
        read_only_fields = ["id", "human_resource_id"]

    def get_reports_relation(self, obj):
        if not obj.reports_to.exists():
            return []
        return [f"{obj.position}-{person.position}" for person in obj.reports_to.all()]

    def get_coops_relation(self, obj):
        if not obj.cooperates_with.exists():
            return []
        return [f"{obj.position}-{person.position}" for person in obj.cooperates_with.all()]


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


class SWOTOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = ['id', 'name', 'custom_name']
        read_only_fields = ['id', 'custom_name']

    def to_representation(self, instance):
        return {'id': instance.id, 'name': instance.name} if instance.name else {'id': instance.id, 'name': instance.custom_name}

    def __init__(self, *args, **kwargs):
        model = kwargs.pop('model', None)
        super().__init__(*args, **kwargs)
        if model:
            self.Meta.model = model


class SWOTStrengthOptionSerializer(SWOTOptionSerializer):
    class Meta(SWOTOptionSerializer.Meta):
        model = SWOTStrengthOption


class SWOTWeaknessOptionSerializer(SWOTOptionSerializer):
    class Meta(SWOTOptionSerializer.Meta):
        model = SWOTWeaknessOption


class SWOTOpportunityOptionSerializer(SWOTOptionSerializer):
    class Meta(SWOTOptionSerializer.Meta):
        model = SWOTOpportunityOption


class SWOTThreatOptionSerializer(SWOTOptionSerializer):
    class Meta(SWOTOptionSerializer.Meta):
        model = SWOTThreatOption


class SWOTMatrixSerializer(serializers.ModelSerializer):
    strengths = SWOTStrengthOptionSerializer(many=True)
    weaknesses = SWOTWeaknessOptionSerializer(many=True)
    opportunities = SWOTOpportunityOptionSerializer(many=True)
    threats = SWOTThreatOptionSerializer(many=True)

    class Meta:
        model = SWOTMatrix
        fields = ['id', 'strengths', 'weaknesses', 'opportunities',
                  'threats', 'create_at', 'updated_at']
        read_only_fields = ['id', 'create_at', 'updated_at']

