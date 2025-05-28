from dateutil.relativedelta import relativedelta


from django.contrib.auth import get_user_model
from django.db import IntegrityError


from rest_framework.exceptions import ValidationError
from rest_framework import serializers


from apps.company.models import (
    CompanyProfile,
    CompanyService,
    License,
    LifeCycleDecline,
    LifeCycleFeature,
    LifeCycleGrowth,
    LifeCycleIntroduction,
    LifeCycleMaturity,
    LifeCycleQuantitative,
    LifeCycleTheoretical,
)

from apps.core.models import Service

User = get_user_model()


class CompanyServiceSerializer(serializers.Serializer):
    service_name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=20, decimal_places=0)
    is_active = serializers.BooleanField()
    purchased_date = serializers.DateField(allow_null=True)


class CompanyProfileSerializer(serializers.ModelSerializer):
    user_national_code = serializers.CharField(
        source="user.national_code", read_only=True
    )
    services = serializers.SerializerMethodField()
    license = serializers.PrimaryKeyRelatedField(
        many=True, queryset=License.objects.all()
    )

    class Meta:
        model = CompanyProfile
        fields = [
            "user_national_code",
            "id",
            "company_title",
            "manager_social_code",
            "manager_phone_number",
            "office_phone_number",
            "email",
            "manager_name",
            "license",
            "special_field",
            "tech_field",
            "province",
            "city",
            "insurance_list",
            "capital_providing_method",
            "is_active",
            "address",
            "services",
        ]

    def get_services(self, company) -> list[str]:
        # Retrieve all services available
        all_services = Service.objects.filter(service_active=True)

        # Get active services for this company
        company_services = CompanyService.objects.filter(company=company)
        active_services = {cs.service_id: cs for cs in company_services if cs.is_active}
        # Format the response data for each service
        services_data = [
            {
                "id": service.id,
                "service_name": service.name,
                "description": service.description,
                # 'price': service.price,
                "is_active": service.id in active_services,
                "purchased_date": (
                    active_services[service.id].purchased_date
                    if service.id in active_services
                    else None
                ),
                "expiration_date": (
                    active_services[service.id].purchased_date + relativedelta(months=3)
                    if service.id in active_services
                    else None
                ),
            }
            for service in all_services
        ]

        return services_data


# TODO : if user service time is expired the service will be removed


class CompanyProfileCreateSerializer(serializers.ModelSerializer):
    license = serializers.PrimaryKeyRelatedField(
        many=True, queryset=License.objects.all()
    )

    class Meta:
        model = CompanyProfile
        fields = [
            "id",
            "company_title",
            "manager_social_code",
            "manager_phone_number",
            "office_phone_number",
            "email",
            "manager_name",
            "license",
            "special_field",
            "tech_field",
            "province",
            "city",
            "insurance_list",
            "capital_providing_method",
            "is_active",
            "address",
        ]

    def validate_email(self, value):
        profile_id = self.instance.id if self.instance else None

        if CompanyProfile.objects.filter(email=value).exclude(id=profile_id).exists():
            raise ValidationError(
                "This email is already associated with another company profile."
            )
        return value

    def validate_social_code(self, value):
        profile_id = self.instance.id if self.instance else None

        if (
            CompanyProfile.objects.filter(social_code=value)
            .exclude(id=profile_id)
            .exists()
        ):
            raise ValidationError(
                "This Social Code is already associated with another company profile."
            )
        return value

    def create(self, validated_data):
        capital_providing_methods = validated_data.pop("capital_providing_method", [])
        license = validated_data.pop("license", [])
        user = self.context["request"].user

        try:
            company_profile, created = CompanyProfile.objects.get_or_create(
                user=user, defaults=validated_data
            )

            if not created:
                for attr, value in validated_data.items():
                    setattr(company_profile, attr, value)
                company_profile.save()

            company_profile.capital_providing_method.set(capital_providing_methods)
            company_profile.license.set(license)
            return company_profile

        except IntegrityError:
            raise ValidationError(
                {
                    "email": "A company profile with this email or social code already exists."
                }
            )

    def update(self, instance, validated_data):
        capital_providing_methods = validated_data.pop("capital_providing_method", [])
        license = validated_data.pop("license", [])

        if "email" in validated_data:
            self.validate_email(validated_data["email"])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        try:
            instance.save()
            if license is not None:
                instance.license.set(license)

            if capital_providing_methods is not None:
                instance.capital_providing_method.set(capital_providing_methods)
            return instance

        except IntegrityError:
            raise ValidationError(
                {"email": "A company profile with this email already exists."}
            )


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
            company = CompanyProfile.objects.get(user=user)
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
            company = CompanyProfile.objects.get(user=user)
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
            company = CompanyProfile.objects.get(user=user)
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
            company = CompanyProfile.objects.get(user=user)
        except CompanyProfile.DoesNotExist:
            raise serializers.ValidationError("No company profile found for the user.")

        validated_data["company"] = company
        resources = validated_data.pop("resource", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.resource.set(resources)
        return instance
