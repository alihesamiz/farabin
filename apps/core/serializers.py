from django.contrib.auth import get_user_model  # type: ignore


from rest_framework import serializers  # type: ignore

from apps.core.models import City, Province
from constants.validators import Validator as _validator


User = get_user_model()


class OTPSendSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    social_code = serializers.CharField(max_length=11)

    def validate_phone_number(self, value):
        return _validator.validate_phone_number(value)

    def validate_social_code(self, value):
        return _validator.validate_social_code(value)


class OTPVerifySerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    otp_code = serializers.CharField()

    def validate_phone_number(self, value):
        return _validator.validate_phone_number(value)

    def validate_otp_code(self, value):
        return _validator.validate_otp_code(value)


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    password = serializers.CharField()

    def validate_phone_number(self, value):
        return _validator.validate_phone_number(value)


class PasswordResetSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()
    new_password2 = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "social_code",
        ]


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "social_code",
        ]
        read_only_filelds = [
            "id",
        ]

    def validate_phone_number(self, value):
        return _validator.validate_phone_number(value)

    def validate_social_code(self, value):
        return _validator.validate_social_code(value)


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = [
            "id",
            "name",
        ]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = [
            "id",
            "name",
            "province",
        ]
