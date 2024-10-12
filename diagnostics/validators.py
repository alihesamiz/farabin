from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

phone_number_validator = RegexValidator(
    regex=r'^09\d{9}$',
    message=_("Phone number must be in 09XXXXXXXXX format."),
    code=_("Invalid_phone_number")
)
