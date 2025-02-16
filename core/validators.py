from django.core.validators import RegexValidator,FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

phone_number_validator = RegexValidator(
    regex=r'^09\d{9}$',
    message=_("Phone number must be in 09XXXXXXXXX format."),
    code=_("Invalid_phone_number")
)


def pdf_file_validator(value):
    
    FileExtensionValidator(['pdf'])(value)

    
    max_file_size = 2 * 1024 * 1024  
    if value.size > max_file_size:
        raise ValidationError(
            f"File size should not exceed 1 MB. Current size: {value.size / (1024 * 1024):.2f} MB.")


def image_file_validator(value):

    FileExtensionValidator(['jpg', 'png', 'jpeg'])(value)

    max_file_size = 2 * 1024 * 1024
    if value.size > max_file_size:
        raise ValidationError(
            _(f"File size should be less than {max_file_size}"))


def ticket_file_validator(value):
    FileExtensionValidator(['pdf', 'jpg', 'png', 'jpeg'])(value)
    max_file_size = 2 * 1024 * 1024
    if value.size > max_file_size:
        raise ValidationError(
            _(f"File size should be less than {max_file_size}"))


def excel_file_validator(value):
    FileExtensionValidator(['xlsx', 'xls', 'csv'])(value)
    max_file_size = 20 * 1024 * 1024
    if value.size > max_file_size:
        raise ValidationError(
            _(f"File size should be less than {max_file_size}"))
