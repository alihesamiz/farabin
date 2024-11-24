from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
User = get_user_model()
 

class OTPSendSerializer(serializers.Serializer):
    # Adjust max_length based on your requirements
    phone_number = serializers.CharField(max_length=11)
    national_code = serializers.CharField(max_length=11)

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

    def validate_national_code(self, value):
        if not value.isdigit():
            raise ValidationError({
                'error_code': 'invalid_national_code',
                'message': _("National Code must contain only digits."),
                'field': 'national_code'
            })
        if len(value) != 11:  # Assuming Iranian phone numbers
            raise ValidationError({
                'error_code': 'invalid_length',
                'message': _("National Code must be 11 digits long."),
                'field': 'national_code'
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
