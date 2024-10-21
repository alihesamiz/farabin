from rest_framework.exceptions import ValidationError

from rest_framework import serializers

from django.contrib.auth import get_user_model

from django.utils.translation import gettext_lazy as _

from .models import CompanyProfile, Dashboard

User = get_user_model()


class CompanyProfileSerializer(serializers.ModelSerializer):
    user_national_code = serializers.CharField(
        source='user.national_code', read_only=True)

    class Meta:
        model = CompanyProfile

        fields = ['company_title', 'user_national_code', 'email', 'social_code',
                  'manager_name', 'license', 'work_place', 'tech_field', 'special_filed', 'insurance_list', 'organization', 'capital_providing_method', 'profile_active']

        read_only_fields = ['user_national_code']

    def validate_email(self, value):
        if CompanyProfile.objects.filter(email=value).exists():
            raise ValidationError({
                'error_code': 'email_exists',
                'message': _("A company with this email already exists."),
                'field': 'email'
            })
        return value

    def validate_social_code(self, value):
        if CompanyProfile.objects.filter(social_code=value).exists():
            raise ValidationError({
                'error_code': 'social_code_exists',
                'message': _("A company with this social code already exists."),
                'field': 'social_code'
            })
        return value


class CompanyProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = ['company_title', 'email', 'social_code',
                  'manager_name', 'license', 'work_place', 'tech_field', 'special_filed', 'insurance_list', 'organization', 'capital_providing_method', 'profile_active']

    def create(self, validated_data):
        # We do not pass 'user' here since it's provided in the view
        return CompanyProfile.objects.create(**validated_data)

    def validate_email(self, value):
        if CompanyProfile.objects.filter(email=value).exists():
            raise ValidationError({
                'error_code': 'email_exists',
                'message': _("A company with this email already exists."),
                'field': 'email'
            })
        return value

    def validate_social_code(self, value):
        if CompanyProfile.objects.filter(social_code=value).exists():
            raise ValidationError({
                'error_code': 'social_code_exists',
                'message': _("A company with this social code already exists."),
                'field': 'social_code'
            })
        return value


class DashboardSerializer(serializers.ModelSerializer):
    company_title = serializers.CharField(
        source='company_service.company.company_title', read_only=True)
    service_name = serializers.CharField(
        source='company_service.service.name', read_only=True)
    is_active = serializers.BooleanField(
        source='company_service.is_active', read_only=True)
    purchased_date = serializers.DateTimeField(
        source='company_service.purchased_date', read_only=True)

    class Meta:
        model = Dashboard
        fields = ['id', 'company_title', 'service_name',
                  'is_active', 'purchased_date']
