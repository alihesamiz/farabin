from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, AuthUser
from rest_framework_simplejwt.tokens import Token
from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import OTP, CompanyProfile
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'national_code', 'phone_number']

    def create(self, validated_data):
        phone_number = validated_data.get('phone_number')
        national_code = validated_data.get('national_code')
        user, created = User.objects.get_or_create(
            national_code=national_code, phone_number=phone_number)

        if created:
            user.set_unusable_password()  # Set a temporary password
            user.save()

        return user


class OTPSendSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)  # Adjust max_length based on your requirements



class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)  # Adjust max_length as necessary
    otp_code = serializers.CharField()


class CompanyProfileSerializer(serializers.ModelSerializer):
    user_national_code = serializers.CharField(
        source='user.national_code', read_only=True)

    class Meta:
        model = CompanyProfile
        fields = ['company_title', 'user_national_code', 'email', 'social_code',
                  'manager_name', 'license', 'work_place', 'tech_field', 'insurance_list', 'organization']
        read_only_fields = ['user_national_code']


class CompanyProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyProfile
        fields = ['company_title', 'email', 'social_code',
                  'manager_name', 'license', 'work_place', 'tech_field', 'insurance_list', 'organization']

    def create(self, validated_data):
        # We do not pass 'user' here since it's provided in the view
        return CompanyProfile.objects.create(**validated_data)
