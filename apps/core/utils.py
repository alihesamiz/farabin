import json
import logging
import os
import re
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
import requests
from django.conf import settings
from django.core.files.storage import default_storage
from django.db import models
from django.db.models.base import Model
from django.utils.deconstruct import deconstructible

from apps.core.models import User

logger = logging.getLogger("core")


@deconstructible
class GeneralUtils:
    SMS_URL = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"
    GREEN = "\033[92m"
    RESET = "\033[0m"

    EXCEPTION_MODELS = settings.FILE_PATH_EXCEPTION_MODELS

    SMS_AUTH_HEADER = {
        "apikey": os.getenv("FARABIN_SMS_API_KEY"),
        "Content-Type": "application/json",
    }

    def __init__(self, path=None, fields=None) -> None:
        self.path = path
        self.fields = fields

    def generate_otp(self):
        """Generate a 6-digit OTP."""
        otp = str(np.random.randint(100000, 999999))
        logger.info(f"Generated OTP: {otp}")
        return otp

    def send_otp(self, phone_number, otp):
        """Send OTP to the given phone number (placeholder for SMS integration)."""
        logger.info(f"Sending OTP {otp} to {phone_number}")

        payload = json.dumps(
            {
                "code": os.getenv("FARABIN_OTP_PATTERN"),
                "sender": "+983000505",
                "recipient": phone_number,
                "variable": {"verification-code": int(otp)},
            }
        )

        try:
            response = requests.post(
                self.SMS_URL, headers=self.SMS_AUTH_HEADER, data=payload
            )
            response.raise_for_status()
            logger.info(f"OTP sent successfully to {phone_number}")
        except requests.RequestException as e:
            logger.error(f"Failed to send OTP to {phone_number}: {e}")
            return None

        return response.text

    def persian_slugify(self, value: str):
        """Slugify a string, keeping Persian characters and numbers."""
        original_value = value
        value = value.strip()
        value = re.sub(r"[\s]+", "-", value)
        value = value.strip("-")
        logger.info(f"Slugified '{original_value}' to '{value}'")
        return value

    def rename_folder(self, instance, filename: str):
        """
        Dynamically rename the file based on the company's name, year, and the field name.
        If the company's name has changed, rename the folder structure accordingly.
        """
        ext = filename.split(".")[-1].lower()

        field_values = []
        for field in self.fields:
            attrs = field.split("__")
            value = instance

            try:
                for attr in attrs:
                    value = getattr(value, attr)

            except AttributeError:
                value = ""
                break

            field_values.append(str(value))

        base_filename = self.persian_slugify("-".join(field_values))

        if not base_filename:
            base_filename = "file"

        current_slug = "file"
        if instance._meta.model.__name__ not in self.EXCEPTION_MODELS:
            try:
                if hasattr(instance.company, "id"):
                    current_slug = instance.company.id

            except Exception:
                current_slug = (
                    instance.issuer.id
                    if hasattr(instance.issuer, "id")
                    else "default-company"
                )

        else:
            current_slug = str(instance._meta.model.__name__)

        year = getattr(instance, "year", "")
        month = getattr(instance, "month", "")

        previous_slug = getattr(instance, "_previous_company_slug", current_slug)

        if previous_slug != current_slug:
            old_folder_path = f"{self.path}/{previous_slug}/{year}"
            new_folder_path = f"{self.path}/{current_slug}/{year}"

            if month:
                old_folder_path += f"/{month}"
                new_folder_path += f"/{month}"

            if default_storage.exists(old_folder_path):
                logger.info(
                    f"Renaming folder from {old_folder_path} to {new_folder_path}"
                )
                default_storage.move(old_folder_path, new_folder_path)

        field_name = "unknown-field"
        for field in instance._meta.fields:
            if isinstance(field, models.FileField):
                file_field = getattr(instance, field.name, None)
                if (
                    file_field
                    and hasattr(file_field, "name")
                    and file_field.name == filename
                ):
                    field_name = field.name
                    break

        if year != "":
            if month:
                final_path = f"{self.path}/{current_slug}/{year}/{month}/{
                    base_filename
                }-{field_name}.{ext}"
            else:
                final_path = f"{self.path}/{current_slug}/{year}/{base_filename}-{
                    field_name
                }.{ext}"

        else:
            final_path = (
                f"{self.path}/{current_slug}/{base_filename}-{field_name}.{ext}"
            )

        logger.info(f"Renamed file to: {final_path}")

        setattr(instance, "_previous_company_slug", current_slug)

        return final_path

    def send_sms(self, instance, message):
        editors = User.objects.filter(groups=1).values_list("phone_number", flat=True)
        phone_numbers = list(editors)

        if not phone_numbers:
            logger.warning("No editors found to send SMS.")
            return

        payload = json.dumps(
            {
                "code": "0vdhr2n9d5b2j78",
                "sender": "+983000505",
                "recipient": phone_numbers,
                "variable": {"verification-code": ""},
            }
        )

        try:
            response = requests.post(
                self.SMS_URL, headers=self.SMS_AUTH_HEADER, data=payload
            )
            response.raise_for_status()
            logger.info(f"SMS sent successfully to {phone_numbers}")
        except requests.RequestException as e:
            logger.error(f"Failed to send SMS: {e}")
            return None

        return response.text

    def deconstruct(self):
        return ("core.GeneralUtils", [self.path, self.fields], {})


class ModelExcelReader:
    """
    ModelExcelReader

    This class takes a Django model and an instance of that model, reads an Excel file
    (from the specified file field on the instance), and creates model objects based on the
    Excel data. It optionally allows you to define which model fields to read,
    or automatically uses all editable fields.

    Parameters:
    ----------
    model : Model
        The Django model class to create objects for. Must inherit from `django.db.models.Model`.

    instance : Model
        An instance of the provided Django model. The Excel file will be read from
        the specified `file_field` on this instance.

    model_field_to_read : Optional[List[str]], default=None
        A list of field names on the model to read from the Excel file. If not provided,
        all editable and non-auto-created fields on the model will be used.

    file_field : str, default="file"
        The name of the file field on the instance that points to the Excel file.

    *args, **kwargs :
        Additional arguments and keyword arguments passed to support extensibility.

    Example:
    -------
    >>> reader = ModelExcelReader(YourModel, instance)
    >>> is_created, msg = reader.create_instances()
    >>> print(msg)
    """

    def __init__(
        self,
        model: Model,
        company_id: str,
        file_path: str,
        model_field_to_read: Optional[List] = None,
        file_field: str = "file",
        *args,
        **kwargs,
    ):
        self.model = model
        self.company_id = company_id
        self.file_path = file_path
        if model_field_to_read and isinstance(model_field_to_read, list):
            self.fields = model_field_to_read
        else:
            self.fields = self._get_model_fields()

    def _get_model_fields(self):
        return [field.name for field in self.model._meta.fields]

    def read_excel(self):
        try:
            df = pd.read_excel(self.file_path)
        except Exception as e:
            raise ValueError(f"Error reading Excel file: {e}")

        model_columns = [col for col in df.columns if col in self.fields]

        if not model_columns:
            raise ValueError(
                "No matching columns found between the Excel file and model fields."
            )

        return df[model_columns]

    def get_missing_columns(self):
        """
        Returns a list of model fields not present in the Excel file.
        """
        df = pd.read_excel(self.file_path)
        missing = set(self.fields) - set(df.columns)
        return list(missing)

    def create_instance(self) -> Tuple[bool, str]:
        """
        Create model instances from Excel rows and bulk insert them.
        """
        df = self.read_excel()

        objects = [
            self.model(company=self.company_id, **row.dropna().to_dict())
            for _, row in df.iterrows()
        ]

        if not objects:
            return (False, print("No objects to create."))

        self.model.objects.bulk_create(objects)

        return (True, print(f"Inserted {len(objects)} {self.model.__name__} records."))
