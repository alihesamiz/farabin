from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
from django.db import transaction
from django.db import models
from math import log2
from core.models import User
import numpy as np
import requests
import json
import re
import os


@deconstructible
class GeneralUtils:

    # SMS PROVIDER API
    url = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"

    headers = {
        'apikey': 'BXb2ovSeYtiAbfVT26gEb50Dmix_-nhAAQRp2v5yfXs=',
        'Content-Type': 'application/json'
    }

    def __init__(self, path=None, fields=None) -> None:
        self.path = path
        self.fields = fields

    # Generate a 6-digit OTP

    def generate_otp(self):
        """Generate a 6-digit OTP."""
        return str(np.random.randint(100000, 999999))

    # Send OTP SMS using the SMS provider API
    def send_otp(self, phone_number, otp):
        """Send OTP to the given phone number (placeholder for SMS integration)."""

        with transaction.atomic():
            payload = json.dumps({
                "code": "0vdhr2n9d5b2j78",
                "sender": "+983000505",
                "recipient": phone_number,
                "variable": {
                    "verification-code": int(otp)
                }
            })

            response = requests.request(
                "POST", self.url, headers=self.headers, data=payload)

        print(f"Sending OTP {otp} to {phone_number}")
        return response.text

    # SLUGIFY a string, keeping Persian characters and numbers.
    def persian_slugify(self, value: str):
        """Slugify a string, keeping Persian characters and numbers."""
        # Remove extra spaces
        value = value.strip()
        # Replace spaces with hyphens
        value = re.sub(r'[\s]+', '-', value)
        return value.strip('-')

    # RENAME a file based on the company's name, year, and the field name.

    def rename_folder(self, instance, filename: str):
        """
        Dynamically rename the file based on the company's name, year, and the field name.
        Files are uploaded into directories based on company name, year, and field name.
        """
        # Get the file extension
        ext = filename.split('.')[-1].lower()

        # Collect the field values for filename generation (company name and year)
        field_values = []
        for field in self.fields:
            attrs = field.split('__')
            value = instance
            try:
                for attr in attrs:
                    value = getattr(value, attr)
            except AttributeError:
                value = ''
                break
            field_values.append(str(value))

        # Slugify the field values (company name and year)
        base_filename = self.persian_slugify("-".join(field_values))

        # Ensure the filename is not empty
        if not base_filename:
            base_filename = 'file'

        # Create the path for the file upload: financial_files/company_name/year/
        company_title = getattr(
            instance.company, 'company_title', 'default-company')
        company_slug = self.persian_slugify(company_title)
        year = getattr(instance, 'year', 'unknown-year')
        month: str = getattr(instance, 'month', '')

        # ** Include the field name in the final file name **
        field_name = 'unknown-field'

        # Find the field that is calling this function based on the filename
        for field in instance._meta.fields:
            # Only check FileField fields
            if isinstance(field, models.FileField):
                file_field = getattr(instance, field.name, None)
                if file_field and hasattr(file_field, 'name') and file_field.name == filename:
                    field_name = field.name
                    break

        # Final path for the file
        print(month)
        if month:
            print(month)

            final_path = f"{
                self.path}/{company_slug}/{year}/{month}/{base_filename}-{field_name}.{ext}"

            print(final_path)
        final_path = f"{
            self.path}/{company_slug}/{year}/{base_filename}-{field_name}.{ext}"

        return final_path

    def send_sms(self, instance, message):

        editors = User.objects.filter(
            groups=1).values_list('phone_number', flat=True)

        with transaction.atomic():
            payload = json.dumps({
                "code": "0vdhr2n9d5b2j78",
                "sender": "+983000505",
                "recipient": [editors],
                "variable": {
                    "verification-code": ""
                }
            })

            response = requests.request(
                "POST", self.url, headers=self.headers, data=payload)

        print(f"Sending {message}to {editors}")

        return response.text

        # TODO: Implement the SMS sending logic here using the SMS provider API.
        pass
