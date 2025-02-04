import numpy as np
import requests
import json
import re
import os

from django.core.files.storage import default_storage
from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
from django.db import transaction
from django.db import models

from core.models import User



@deconstructible
class GeneralUtils:

    
    SMS_URL = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"
    
    GREEN = "\033[92m"
    
    RESET = "\033[0m"

    EXCEPTION_MODELS=["OrganizationChart"]
    
    SMS_AUTH_HEADER = {
        'apikey': os.getenv('FARABIN_SMS_API_KEY','BXb2ovSeYtiAbfVT26gEb50Dmix_-nhAAQRp2v5yfXs='),
        'Content-Type': 'application/json'
    }

    def __init__(self, path=None, fields=None) -> None:
        self.path = path
        self.fields = fields

    def generate_otp(self):
        """Generate a 6-digit OTP."""
        return str(np.random.randint(100000, 999999))

    def send_otp(self, phone_number, otp):
        """Send OTP to the given phone number (placeholder for SMS integration)."""

        with transaction.atomic():
            payload = json.dumps({
                "code": os.getenv("FARABIN_OTP_PATTERN","0vdhr2n9d5b2j78"),
                "sender": "+983000505",
                "recipient": phone_number,
                "variable": {
                    "verification-code": int(otp)
                }
            })

            response = requests.request(
                "POST", self.SMS_URL, headers=self.SMS_AUTH_HEADER, data=payload)

        print(f"{self.GREEN}Sending OTP {otp} to {phone_number}")
        
        return response.text

    def persian_slugify(self, value: str):
        """Slugify a string, keeping Persian characters and numbers."""

        value = value.strip()

        value = re.sub(r'[\s]+', '-', value)

        return value.strip('-')

    def rename_folder(self, instance, filename: str):
        """
        Dynamically rename the file based on the company's name, year, and the field name.
        If the company's name has changed, rename the folder structure accordingly.
        """
        
        ext = filename.split('.')[-1].lower()

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

        base_filename = self.persian_slugify("-".join(field_values))

        if not base_filename:
            base_filename = 'file'
            
        if instance._meta.model.__name__ not in self.EXCEPTION_MODELS:
            try:
                if hasattr(instance.company, 'id'):
                    current_slug = instance.company.id

            except:
                current_slug = instance.issuer.id if hasattr(
                    instance.issuer, 'id') else 'default-company'

        else:
            current_slug = 'organization_excel_files'

        year = getattr(instance, 'year', '')
        month = getattr(instance, 'month', '')
        
        previous_slug = getattr(
            instance, '_previous_company_slug', current_slug)

        
        if previous_slug != current_slug:
            old_folder_path = f"{self.path}/{previous_slug}/{year}"
            new_folder_path = f"{self.path}/{current_slug}/{year}"

            if month:
                old_folder_path += f"/{month}"
                new_folder_path += f"/{month}"
            
            if default_storage.exists(old_folder_path):
                default_storage.move(old_folder_path, new_folder_path)
        
        field_name = 'unknown-field'
        for field in instance._meta.fields:
            
            if isinstance(field, models.FileField):
                file_field = getattr(instance, field.name, None)
                if file_field and hasattr(file_field, 'name') and file_field.name == filename:
                    field_name = field.name
                    break
        
        if year != "":
            if month:
                final_path = f"{
                    self.path}/{current_slug}/{year}/{month}/{base_filename}-{field_name}.{ext}"
            else:
                final_path = f"{
                    self.path}/{current_slug}/{year}/{base_filename}-{field_name}.{ext}"
        
        else:
            final_path = f"{
                self.path}/{current_slug}/{base_filename}-{field_name}.{ext}"
        
        setattr(instance, '_previous_company_slug', current_slug)

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
                "POST", self.SMS_URL, headers=self.SMS_AUTH_HEADER, data=payload)
        
        
        print(f"Sending {message}to {editors}")

        return response.text

    def deconstruct(self):
        return (
            'core.GeneralUtils',
            [self.path, self.fields],
            {}
        )
