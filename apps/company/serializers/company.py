from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
    SlugField,
    SlugRelatedField,
)

from apps.company.models import (
    CompanyProfile,
    CompanyUser,
    License,
    SpecialTech,
    TechField,
)
from constants.validators import Validator as _validator

User = get_user_model()


class UserProfileSerializer(ModelSerializer):
    role = CharField(max_length=11, required=False)

    class Meta:
        model = User
        fields = [
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
    class Meta:
        model = CompanyUser
        fields = [
            "role",
            "updated_at",
            "deleted_at",
        ]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


class CompanyProfileSerializer(ModelSerializer):
    tech_field = SlugRelatedField(
        slug_field="name",
        queryset=TechField.objects.all(),
    )
    special_field = SlugRelatedField(
        slug_field="name",
        queryset=SpecialTech.objects.all(),
    )
    license = SlugRelatedField(
        slug_field="name",
        queryset=License.objects.all(),
        many=True,
    )
    capital_providing_method = SerializerMethodField()
    province = SlugField()
    city = SlugField()

    def get_capital_providing_method(self, obj):
        return [item.get_name_display() for item in obj.capital_providing_method.all()]

    class Meta:
        model = CompanyProfile
        fields = [
            "id",
            "title",
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
        ]


class CompanyProfileCreateSerializer(ModelSerializer):
    license = PrimaryKeyRelatedField(many=True, queryset=License.objects.all())

    class Meta:
        model = CompanyProfile
        fields = [
            "id",
            "title",
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
        ]

    # def validate_email(self, value):
    #     profile_id = self.instance.id if self.instance else None

    #     if CompanyProfile.objects.filter(email=value).exclude(id=profile_id).exists():
    #         raise ValidationError(
    #             "This email is already associated with another company profile."
    #         )
    #     return value


    def validate_social_code(self, value):
        return _validator.validate_social_code(value)

    def create(self, validated_data):
        capital_providing_methods = validated_data.pop("capital_providing_method", [])
        licenses = validated_data.pop("license", [])
        # user = self.context["request"].user
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

    # def update(self, instance, validated_data):
    #     capital_providing_methods = validated_data.pop("capital_providing_method", [])
    #     licenses = validated_data.pop("license", [])

    #     if "email" in validated_data:
    #         self.validate_email(validated_data["email"])

    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)

    #     try:
    #         instance.save()

    #         if licenses is not None:
    #             instance.license.set(licenses)

    #         if capital_providing_methods is not None:
    #             instance.capital_providing_method.set(capital_providing_methods)

    #         return instance

    #     except IntegrityError:
    #         raise ValidationError(
    #             {"email": "A company profile with this email already exists."}
    #         )


class CompanyProfileUpdateSerializer(ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = [
            "id",
            "title",
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
            "is_active",
        ]
        read_only_fields = ["id"]

    def update(self, instance: CompanyProfile, validated_data):
        licenses = validated_data.pop("license", None)
        capital_providing_methods = validated_data.pop("capital_providing_method", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if licenses is not None:
            instance.license.set(licenses)
        if capital_providing_methods is not None:
            instance.capital_providing_method.set(capital_providing_methods)

        instance.save()

        return super().update(instance, validated_data)


# class CompanyProfileUpdateSerializer(ModelSerializer): ...
