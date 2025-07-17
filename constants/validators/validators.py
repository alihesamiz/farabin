from django.core.validators import (
    RegexValidator,
    FileExtensionValidator,
    MinValueValidator,
    MaxValueValidator,
)
from rest_framework.exceptions import ValidationError


class Validator:
    @classmethod
    def validate_phone_number(cls, value):
        if not value.isdigit():
            raise ValidationError(
                {
                    "error_code": "invalid_phone_number",
                    "message": "Phone number must contain only digits.",
                    "field": "phone_number",
                }
            )
        if len(value) != 11:
            raise ValidationError(
                {
                    "error_code": "invalid_length",
                    "message": "Phone number must be 11 digits long.",
                    "field": "phone_number",
                }
            )
        return value

    @classmethod
    def validate_social_code(cls, value):
        if not value.isdigit():
            raise ValidationError(
                {
                    "error_code": "invalid_social_code",
                    "message": "National Code must contain only digits.",
                    "field": "social_code",
                }
            )
        if len(value) != 10:
            raise ValidationError(
                {
                    "error_code": "invalid_length",
                    "message": "National Code must be 10 digits long.",
                    "field": "social_code",
                }
            )
        return value

    @classmethod
    def validate_otp_code(cls, value):
        if not value.isdigit():
            raise ValidationError(
                {
                    "error_code": "invalid_otp_code",
                    "message": "OTP code must contain only digits.",
                    "field": "otp_code",
                }
            )
        if len(value) != 6:
            raise ValidationError(
                {
                    "error_code": "invalid_length",
                    "message": "OTP code must be 6 digits long.",
                    "field": "otp_code",
                }
            )
        return value

    @classmethod
    def phone_number_model_regex_validator(cls) -> RegexValidator:
        return RegexValidator(
            regex=r"^09\d{9}$",
            message="Phone number must be in 09XXXXXXXXX format.",
            code="Invalid_phone_number",
        )

    @classmethod
    def landline_number_model_regex_validator(cls) -> RegexValidator:
        return RegexValidator(
            regex=r"^0\d{10}$",
            message="Phone number must be in 09XXXXXXXXX format.",
            code="Invalid_phone_number",
        )

    @classmethod
    def pdf_file_validator(cls, value):
        FileExtensionValidator(["pdf"])(value)

        max_file_size = 2 * 1024 * 1024
        if value.size > max_file_size:
            raise ValidationError(
                f"File size should not exceed 1 MB. Current size: {value.size / (1024 * 1024):.2f} MB."
            )

    @classmethod
    def image_file_validator(cls, value):
        FileExtensionValidator(["jpg", "png", "jpeg"])(value)

        max_file_size = 2 * 1024 * 1024
        if value.size > max_file_size:
            raise ValidationError(f"File size should be less than {max_file_size}")

    @classmethod
    def ticket_file_validator(cls, value):
        FileExtensionValidator(["pdf", "jpg", "png", "jpeg"])(value)
        max_file_size = 2 * 1024 * 1024
        if value.size > max_file_size:
            raise ValidationError(f"File size should be less than {max_file_size}")

    @classmethod
    def excel_file_validator(cls, value):
        FileExtensionValidator(["xlsx", "xls", "csv"])(value)
        max_file_size = 20 * 1024 * 1024
        if value.size > max_file_size:
            raise ValidationError(f"File size should be less than {max_file_size}")

    @classmethod
    def min_numeric_value_validator(cls, value=0):
        return MinValueValidator(
            value, message=f"No Value less than {value} are allowed"
        )

    @classmethod
    def max_numeric_value_validator(cls, value=10):
        return MaxValueValidator(
            value, message=f"No Value greater than {value} are allowed"
        )
