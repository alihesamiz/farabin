from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
User = get_user_model()


# class UserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = ['id', 'national_code', 'phone_number']

#     def validate(self, data):
#         national_code = data.get('national_code')
#         phone_number = data.get('phone_number')

#         if User.objects.filter(national_code=national_code).exists():
#             raise ValidationError({
#                 'error_code': 'national_code_exists',
#                 'message': _("A user with this national code already exists."),
#                 'field': 'national_code'
#             })

#         if User.objects.filter(phone_number=phone_number).exists():
#             raise ValidationError({
#                 'error_code': 'phone_number_exists',
#                 'message': _("A user with this phone number already exists."),
#                 'field': 'phone_number'
#             })

#         return data

#     def create(self, validated_data):
#         # phone_number = validated_data.get('phone_number')
#         # national_code = validated_data.get('national_code')
#         user, created = User.objects.get_or_create(**validated_data)

#         if created:
#             user.set_unusable_password()  # Set a temporary password
#             user.save()

#         return user


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
