import logging

from rest_framework import serializers

from apps.management.models import (
    HumanResource,
    OrganizationChartBase,
    PersonelInformation,
)
import os


logger = logging.getLogger("management")



class HumanResourceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HumanResource
        fields = ["excel_file"]

    def validate_company(self, value):
        human_resource = HumanResource.objects.filter(company=value)
        if human_resource.exists():
            human_resource.delete()
            logger.info(f"Existing HumanResource for company {value} deleted.")

        return value



    def create(self, validated_data):
        company = self.context["company"]

        # Check if there's an existing HR record
        existing_hr = HumanResource.objects.filter(company=company).first()
        if existing_hr:
            # Delete the old file
            if existing_hr.excel_file and os.path.exists(existing_hr.excel_file.path):
                os.remove(existing_hr.excel_file.path)
                logger.info(f"Deleted old Excel file for company {company.title}")
            
            # Update the instance with new file instead of creating a new one
            existing_hr.excel_file = validated_data["excel_file"]
            existing_hr.save()
            
            # Trigger processing
            from .tasks import process_personnel_excel
            process_personnel_excel.delay(existing_hr.id)
            logger.info(f"process_personnel_excel called for updated HR file")
            return existing_hr

        # No existing record, create new
        validated_data["company"] = company
        instance = super().create(validated_data)

        from .tasks import process_personnel_excel
        process_personnel_excel.delay(instance.id)
        logger.info(f"process_personnel_excel called for new HR file")
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
    reports_to = serializers.PrimaryKeyRelatedField(
        queryset=PersonelInformation.objects.all(), many=True, required=False
    )
    cooperates_with = serializers.PrimaryKeyRelatedField(
        queryset=PersonelInformation.objects.all(), many=True, required=False
    )
    reports_relation = serializers.SerializerMethodField()
    coops_relation = serializers.SerializerMethodField()

    class Meta:
        model = PersonelInformation
        fields = [
            'id', 'human_resource', 'name', 'position', 'reports_to',
            'cooperates_with', 'obligations', 'reports_relation', 'coops_relation'
        ]
        read_only_fields = ['id', 'human_resource', 'reports_relation', 'coops_relation']

    def validate(self, data):
        if not data.get('name'):
            raise serializers.ValidationError({"name": "Name is required."})
        if not data.get('position'):
            raise serializers.ValidationError({"position": "Position is required."})
        return data

    def validate_reports_to(self, value):
        company = self.context.get('company')
        if company and value:
            invalid_ids = [
                pid for pid in value
                if not isinstance(pid, int) or not PersonelInformation.objects.filter(id=pid, human_resource__company=company).exists()
            ]
            if invalid_ids:
                raise serializers.ValidationError(f"Invalid reports_to IDs: {invalid_ids}. Must be valid integer IDs.")
        return value

    def validate_cooperates_with(self, value):
        company = self.context.get('company')
        if company and value:
            invalid_ids = [
                pid for pid in value
                if not isinstance(pid, int) or not PersonelInformation.objects.filter(id=pid, human_resource__company=company).exists()
            ]
            if invalid_ids:
                raise serializers.ValidationError(f"Invalid cooperates_with IDs: {invalid_ids}. Must be valid integer IDs.")
        return value

    def create(self, validated_data):
        instance = super().create(validated_data)
        return instance

    def get_reports_relation(self, instance):
        return [
            f"{instance.position}-{reports_to_person.position}"
            for reports_to_person in instance.reports_to.all()
        ]

    def get_coops_relation(self, instance):
        return [
            f"{instance.position}-{coop_person.position}"
            for coop_person in instance.cooperates_with.all()
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
