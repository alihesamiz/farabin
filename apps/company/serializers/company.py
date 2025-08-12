from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
)

from apps.company.models import (
    CompanyProfile,
    CompanyUser,
)
from constants.validators import Validator as _validator

User = get_user_model()


class UserProfileSerializer(ModelSerializer):
    role = CharField(max_length=11, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "social_code",
            "role",
        ]

    def create(self, validated_data):
        validated_data.pop("role", None)
        return super().create(validated_data)


class CompanyUserSerializer(ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    role = CharField(source="get_role_display", read_only=True)

    class Meta:
        model = CompanyUser
        fields = [
            "id",
            "user",
            "role",
            "created_at",
            "updated_at",
            "deleted_at",
        ]


class CompanyUserCreateSerializer(ModelSerializer):
    class Meta:
        model = CompanyUser
        fields = [
            "id",
            "user",
            "role",
            "created_at",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = [
            "created_at",
            "updated_at",
            "deleted_at",
        ]

    def create(self, validated_data):
        validated_data["company"] = self.context["company"]

        return CompanyUser.objects.select_related(
            "user",
            "company",
        ).create(**validated_data)


class CompanyUserUpdateSerializer(ModelSerializer):
    user = UserProfileSerializer(required=False)

    class Meta:
        model = CompanyUser
        fields = [
            "user",
            "role",
            "updated_at",
            "deleted_at",
        ]
        read_only_fields = ["updated_at", "deleted_at"]

    def update(self, instance: CompanyUser, validated_data: dict):
        user_data = validated_data.pop("user", None)
        print(user_data)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()
        instance.save()

        return instance


class CompanyProfileSerializer(ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = [
            "id",
            "title",
            "logo",
            "email",
            "national_code",
            "office_phone_number",
            "license",
            "tech_field",
            "special_field",
            "insurance_list",
            "capital_providing_method",
            "province",
            "city",
            "address",
            "is_profile_complete",
            "upstream_industries",
            "downstream_industries",
        ]


class CompanyProfileCreateSerializer(ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = [
            "id",
            "title",
            "logo",
            "email",
            "national_code",
            "office_phone_number",
            "license",
            "tech_field",
            "special_field",
            "insurance_list",
            "capital_providing_method",
            "province",
            "city",
            "address",
            "upstream_industries",
            "downstream_industries",
        ]

    def validate_social_code(self, value):
        return _validator.validate_social_code(value)

    def create(self, validated_data):
        capital_providing_methods = validated_data.pop("capital_providing_method", [])
        licenses = validated_data.pop("license", [])
        try:
            company_profile = CompanyProfile.objects.create(**validated_data)
            company_profile.capital_providing_method.set(capital_providing_methods)
            company_profile.license.set(licenses)

            return company_profile

        except IntegrityError:
            raise ValidationError(
                {
                    "email": "A company profile with this email or social code already exists."
                }
            )


class CompanyProfileUpdateSerializer(ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = [
            "id",
            "title",
            "logo",
            "email",
            "national_code",
            "office_phone_number",
            "license",
            "tech_field",
            "special_field",
            "insurance_list",
            "capital_providing_method",
            "province",
            "city",
            "address",
            "upstream_industries",
            "downstream_industries",
        ]
        read_only_fields = ["id"]

    def update(self, instance: CompanyProfile, validated_data):
        licenses = validated_data.pop("license", [])
        capital_providing_methods = validated_data.pop("capital_providing_method", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if any(licenses):
            instance.license.set(licenses)
        if any(capital_providing_methods):
            instance.capital_providing_method.set(capital_providing_methods)

        instance.save()

        return super().update(instance, validated_data)
