from django.contrib.auth import get_user_model
from rest_framework import serializers


from apps.company.models import (
    CompanyProfile,
    LifeCycleDecline,
    LifeCycleFeature,
    LifeCycleGrowth,
    LifeCycleIntroduction,
    LifeCycleMaturity,
    LifeCycleQuantitative,
    LifeCycleTheoretical,
)


User = get_user_model()


class LifeCycleFeatureSerializer(serializers.ModelSerializer):
    """Serializer for LifeCycleFeature model"""

    class Meta:
        model = LifeCycleFeature
        fields = ["id", "name", "weight"]


class BaseLifeCycleSerializer(serializers.ModelSerializer):
    """Base serializer for LifeCycle models with id and name fields."""

    class Meta:
        fields = ["id", "name"]


class LifeCycleDeclineSerializer(BaseLifeCycleSerializer):
    """Serializer for LifeCycleDecline model"""

    class Meta(BaseLifeCycleSerializer.Meta):
        model = LifeCycleDecline


class LifeCycleMaturitySerializer(BaseLifeCycleSerializer):
    """Serializer for LifeCycleMaturity model"""

    class Meta(BaseLifeCycleSerializer.Meta):
        model = LifeCycleMaturity


class LifeCycleGrowthSerializer(BaseLifeCycleSerializer):
    """Serializer for LifeCycleGrowth model"""

    class Meta(BaseLifeCycleSerializer.Meta):
        model = LifeCycleGrowth


class LifeCycleIntroductionSerializer(BaseLifeCycleSerializer):
    """Serializer for LifeCycleIntroduction model"""

    class Meta(BaseLifeCycleSerializer.Meta):
        model = LifeCycleIntroduction


class LifeCycleTheoreticalPlaceSerializer(serializers.ModelSerializer):
    """Serializer for LifeCyclePlace model"""

    feature = LifeCycleFeatureSerializer()
    decline = LifeCycleDeclineSerializer()
    maturity = LifeCycleMaturitySerializer()
    growth = LifeCycleGrowthSerializer()
    introduction = LifeCycleIntroductionSerializer()
    company_place = serializers.SerializerMethodField()

    class Meta:
        model = LifeCycleTheoretical
        fields = [
            "id",
            "company",
            "feature",
            "decline",
            "maturity",
            "growth",
            "introduction",
            "company_place",
            "created_at",
            "updated_at",
        ]

    def get_company_place(self, obj: LifeCycleTheoretical):
        return obj._get_weights()


class LifeCycleTheoreticalPlaceCreateUpdateSerializer(
    LifeCycleTheoreticalPlaceSerializer
):
    """Serializer for LifeCyclePlace model"""

    feature = serializers.PrimaryKeyRelatedField(
        queryset=LifeCycleFeature.objects.all()
    )
    decline = serializers.PrimaryKeyRelatedField(
        queryset=LifeCycleDecline.objects.all()
    )
    maturity = serializers.PrimaryKeyRelatedField(
        queryset=LifeCycleMaturity.objects.all()
    )
    growth = serializers.PrimaryKeyRelatedField(queryset=LifeCycleGrowth.objects.all())
    introduction = serializers.PrimaryKeyRelatedField(
        queryset=LifeCycleIntroduction.objects.all()
    )

    class Meta:
        model = LifeCycleTheoretical
        fields = [
            "id",
            "feature",
            "decline",
            "maturity",
            "growth",
            "introduction",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        """Creates a LifeCyclePlace instance with nested objects."""
        user = self.context["request"].user
        try:
            company = CompanyProfile.objects.get(company_user__user=user)
        except CompanyProfile.DoesNotExist:
            raise serializers.ValidationError("No company profile found for the user.")

        validated_data["company"] = company
        life_cycle_place = LifeCycleTheoretical.objects.create(**validated_data)
        return life_cycle_place

    def update(self, instance, validated_data):
        """Updates a LifeCyclePlace instance and its nested objects."""
        # Extract nested data
        user = self.context["request"].user
        try:
            company = CompanyProfile.objects.get(company_user__user=user)
        except CompanyProfile.DoesNotExist:
            raise serializers.ValidationError("No company profile found for the user.")

        validated_data["company"] = company

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class LifeCycleQuantitativePlaceSerializer(serializers.ModelSerializer):
    """Serializer for LifeCycleQuantitativePlace model."""

    class Meta:
        model = LifeCycleQuantitative
        fields = [
            "id",
            "company",
            "resource",
            "place",
            "created_at",
            "updated_at",
        ]


class LifeCycleQuantitativePlaceCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifeCycleQuantitative
        fields = [
            "id",
            "resource",
            "place",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        try:
            company = CompanyProfile.objects.get(company_user__user=user)
        except CompanyProfile.DoesNotExist:
            raise serializers.ValidationError("No company profile found for the user.")

        validated_data["company"] = company
        resources = validated_data.pop("resource", [])
        life_cycle_place = LifeCycleQuantitative.objects.create(**validated_data)
        life_cycle_place.resource.set(resources)
        return life_cycle_place

    def update(self, instance, validated_data):
        """Updates a LifeCyclePlace instance and its nested objects."""
        # Extract nested data
        user = self.context["request"].user
        try:
            company = CompanyProfile.objects.get(company_user__user=user)
        except CompanyProfile.DoesNotExist:
            raise serializers.ValidationError("No company profile found for the user.")

        validated_data["company"] = company
        resources = validated_data.pop("resource", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.resource.set(resources)
        return instance
