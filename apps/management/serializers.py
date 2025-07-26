import logging

from rest_framework import serializers

from apps.management.models import (
    HumanResource,
    OrganizationChartBase,
    PersonelInformation,
    SWOTAnalysis,
    SWOTMatrix,
    SWOTOption,
    SWOTQuestion,
)

logger = logging.getLogger("management")


class HumanResourceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanResource
        fields = ["excel_file"]  # , 'company']

    def validate_company(self, value):
        logger.info(f"Validating company: {value}")
        if HumanResource.objects.filter(company=value).exists():
            logger.warning(f"Company {value} already has a Human Resource record.")
            raise serializers.ValidationError(
                "Each company can only have one Human Resource record."
            )
        logger.info("Company validation passed.")
        return value

    def create(self, validated_data):
        company = self.context["company"]
        validated_data["company"] = company
        instance = super().create(validated_data)

        return instance


class HumanResourceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanResource
        fields = ["excel_file"]
        extra_kwargs = {"excel_file": {"required": False}}


class HumanResourceSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source="company.name", read_only=True)

    class Meta:
        model = HumanResource
        fields = [
            "id",
            "excel_file",
            "company",
            "company_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class PersonelInformationSerializer(serializers.ModelSerializer):
    human_resource_id = serializers.PrimaryKeyRelatedField(
        source="human_resource", read_only=True
    )

    reports_relation = serializers.SerializerMethodField()

    coops_relation = serializers.SerializerMethodField()

    class Meta:
        model = PersonelInformation
        fields = [
            "id",
            "human_resource_id",
            "name",
            "position",
            "reports_to",
            "cooperates_with",
            "obligations",
            "reports_relation",
            "coops_relation",
        ]
        read_only_fields = ["id", "human_resource_id"]

    def get_reports_relation(self, obj):
        logger.info(f"Fetching reports_relation for PersonelInformation ID: {obj.id}")
        if not obj.reports_to.exists():
            return []
        return [f"{obj.position}-{person.position}" for person in obj.reports_to.all()]

    def get_coops_relation(self, obj):
        logger.info(f"Fetching coops_relation for PersonelInformation ID: {obj.id}")
        if not obj.cooperates_with.exists():
            return []
        return [
            f"{obj.position}-{person.position}" for person in obj.cooperates_with.all()
        ]


class ChartNodeSerializer(serializers.ModelSerializer):
    reports_relation = serializers.SerializerMethodField()

    coops_relation = serializers.SerializerMethodField()

    class Meta:
        model = PersonelInformation
        fields = [
            "id",
            "name",
            "position",
            "reports_relation",
            "coops_relation",
            "obligations",
        ]

    def get_reports_relation(self, obj):
        logger.info(f"Fetching reports_relation for ChartNode ID: {obj.id}")
        if not obj.reports_to.exists():
            return []
        return [f"{obj.position}-{person.position}" for person in obj.reports_to.all()]

    def get_coops_relation(self, obj):
        logger.info(f"Fetching coops_relation for ChartNode ID: {obj.id}")
        if not obj.cooperates_with.exists():
            return []
        return [
            f"{obj.position}-{person.position}" for person in obj.cooperates_with.all()
        ]


class PersonelInformationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonelInformation
        fields = ["human_resource", "name", "position", "reports_to", "obligations"]


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
    position_excel_url = serializers.FileField(source="position_excel", read_only=True)

    class Meta:
        model = OrganizationChartBase
        fields = ["id", "position_excel_url"]


class SWOTQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SWOTQuestion
        fields = ["id", "text", "category"]


class SWOTOptionBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SWOTOption
        fields = [
            "id",
            "question",
            "answer",
            "category",
            "external_factor",
            "created_at",
            "updated_at",
        ]


class SWOTOptionSerializer(SWOTOptionBaseSerializer):
    question = serializers.PrimaryKeyRelatedField(queryset=SWOTQuestion.objects.all())
    question_detail = SWOTQuestionSerializer(source="question", read_only=True)

    class Meta(SWOTOptionBaseSerializer.Meta):
        fields = SWOTOptionBaseSerializer.Meta.fields + [
            "question_detail",
        ]


class SWOTOptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SWOTOption
        fields = [
            "question",
            "answer",
            # "category",
            "external_factor",
        ]

    def create(self, validated_data):
        company = self.context["company"]
        validated_data["company"] = company
        instance = super().create(validated_data)

        return instance


class SWOTMatrixSerializer(serializers.ModelSerializer):
    strengths = SWOTOptionSerializer(many=True, read_only=True)
    weaknesses = SWOTOptionSerializer(many=True, read_only=True)
    opportunities = SWOTOptionSerializer(many=True, read_only=True)
    threats = SWOTOptionSerializer(many=True, read_only=True)

    class Meta:
        model = SWOTMatrix
        fields = [
            "id",
            "strengths",
            "weaknesses",
            "opportunities",
            "threats",
            "created_at",
            "updated_at",
        ]


class SWOTAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SWOTAnalysis
        fields = [
            "id",
            "so",
            "st",
            "wo",
            "wt",
            "created_at",
            "updated_at",
        ]
