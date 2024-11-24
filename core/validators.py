from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

phone_number_validator = RegexValidator(
    regex=r'^09\d{9}$',
    message=_("Phone number must be in 09XXXXXXXXX format."),
    code=_("Invalid_phone_number")
)


def pdf_file_validator(value):
    # Check file extension
    FileExtensionValidator(['pdf'])(value)

    # Check file size (1 MB limit)
    max_file_size = 1 * 1024 * 1024  # 1 MB in bytes
    if value.size > max_file_size:
        raise ValidationError(
            f"File size should not exceed 1 MB. Current size: {value.size / (1024 * 1024):.2f} MB.")


def image_file_validator(value):
    
    FileExtensionValidator(['jpg','png','jpeg'])(value)
    
    max_file_size = 2 * 1024 * 1024 
    if value.size> max_file_size :
        raise ValidationError(_(f"File size should be less than {max_file_size}"))