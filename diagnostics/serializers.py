from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import OTP, CompanyProfile, Dashboard
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'national_code', 'phone_number']

    def validate(self, data):
        national_code = data.get('national_code')
        phone_number = data.get('phone_number')

        if User.objects.filter(national_code=national_code).exists():
            raise ValidationError({
                'error_code': 'national_code_exists',
                'message': _("A user with this national code already exists."),
                'field': 'national_code'
            })

        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError({
                'error_code': 'phone_number_exists',
                'message': _("A user with this phone number already exists."),
                'field': 'phone_number'
            })

        return data

    def create(self, validated_data):
        # phone_number = validated_data.get('phone_number')
        # national_code = validated_data.get('national_code')
        user, created = User.objects.get_or_create(**validated_data)

        if created:
            user.set_unusable_password()  # Set a temporary password
            user.save()

        return user


class OTPSendSerializer(serializers.Serializer):
    # Adjust max_length based on your requirements
    phone_number = serializers.CharField(max_length=11)

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise ValidationError({
                'error_code': 'invalid_phone_number',
                'message': _("Phone number must contain only digits."),
                'field': 'phone_number'
            })
        if len(value) != 11:  # Assuming Iranian phone numbers
            raise ValidationError({
                'error_code': 'invalid_length',
                'message': _("Phone number must be 11 digits long."),
                'field': 'phone_number'
            })
        return value


class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        max_length=11)  # Adjust max_length as necessary
    otp_code = serializers.CharField()

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise ValidationError({
                'error_code': 'invalid_phone_number',
                'message': _("Phone number must contain only digits."),
                'field': 'phone_number'
            })
        if len(value) != 11:  # Assuming Iranian phone numbers
            raise ValidationError({
                'error_code': 'invalid_length',
                'message': _("Phone number must be 11 digits long."),
                'field': 'phone_number'
            })
        return value

    def validate_otp_code(self, value):
        if not value.isdigit():
            raise ValidationError({
                'error_code': 'invalid_otp_code',
                'message': _("OTP code must contain only digits."),
                'field': 'otp_code'
            })
        if len(value) != 6:  # Assuming 6-digit OTP
            raise ValidationError({
                'error_code': 'invalid_length',
                'message': _("OTP code must be 6 digits long."),
                'field': 'otp_code'
            })
        return value


class CompanyProfileSerializer(serializers.ModelSerializer):
    user_national_code = serializers.CharField(
        source='user.national_code', read_only=True)

    class Meta:
        model = CompanyProfile
        fields = ['company_title', 'user_national_code', 'email', 'social_code',
                  'manager_name', 'license', 'work_place', 'tech_field', 'insurance_list', 'organization']
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
                  'manager_name', 'license', 'work_place', 'tech_field', 'insurance_list', 'organization']

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
