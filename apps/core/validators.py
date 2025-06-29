from django.core.validators import RegexValidator, FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class Validator:
    @classmethod
    def phone_number_model_regex_validator(cls) -> RegexValidator:
        return RegexValidator(
            regex=r"^09\d{9}$",
            message=_("Phone number must be in 09XXXXXXXXX format."),
            code=_("Invalid_phone_number"),
        )

    @classmethod
    def landline_number_model_regex_validator(cls) -> RegexValidator:
        return RegexValidator(
            regex=r"^0\d{10}$",
            message=_("Phone number must be in 09XXXXXXXXX format."),
            code=_("Invalid_phone_number"),
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
            raise ValidationError(
                _(f"File size should be less than {max_file_size}"))

    @classmethod
    def ticket_file_validator(cls, value):
        FileExtensionValidator(["pdf", "jpg", "png", "jpeg"])(value)
        max_file_size = 2 * 1024 * 1024
        if value.size > max_file_size:
            raise ValidationError(
                _(f"File size should be less than {max_file_size}"))

    @classmethod
    def excel_file_validator(cls, value):
        FileExtensionValidator(["xlsx", "xls", "csv"])(value)
        max_file_size = 20 * 1024 * 1024
        if value.size > max_file_size:
            raise ValidationError(
                _(f"File size should be less than {max_file_size}"))
