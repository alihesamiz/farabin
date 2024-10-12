from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
from math import log2
import numpy as np
import re
import os


def get_life_cycle(financial_assets):
    # Initialize life_cycle and cycles
    x_vals = [_("Start"), _("Introduction"), _("Growth"), _("Maturity"),
              _("Recession 1"), _("Recession 2"), _("Recession 3"),
              _("Decline 1"), _("Decline 2")]
    x_vals_numerical = [1, 1.5, 2, 2.5, 4, 4.5, 4, 3, 2]
    y_vals = [log2(x) for x in x_vals_numerical]

    cycles = []

    # Get the last financial asset
    finance = financial_assets.last()

    # If there are no financial assets, return the default values
    if not finance:
        return 5, x_vals, y_vals

    # Retrieve life_cycles and append their ids to cycles list
    life_cycles = finance.capital_providing_method.all()
    cycles = [lc.id for lc in life_cycles]

    # Dictionary for mapping different cycle combinations to life_cycle values
    cycle_mappings = {
        (1, 2): 7,
        (1, 3): 6,
        (2, 3): 2,
        (1,): 8,
        (2,): 1,
        (3,): 3
    }

    # Determine life_cycle based on the length of cycles
    if len(cycles) == 3:
        life_cycle = 5
    elif len(cycles) == 2:
        life_cycle = cycle_mappings.get(tuple(sorted(cycles)), 0)
    elif len(cycles) == 1:
        life_cycle = cycle_mappings.get(tuple(cycles), 0)
    else:
        life_cycle = 5

    return life_cycle, x_vals, y_vals


@deconstructible
class CustomUtils:
    def __init__(self, path=None, fields=None) -> None:
        self.path = path
        self.fields = fields

    def rename_folder(self, instance, filename: str):
        """Dynamically rename the image based on model fields."""
        ext = filename.split('.')[-1].lower()

        # Collect field values and join them into the filename
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

        # Slugify the filename
        base_filename = self.persian_slugify("-".join(field_values))

        # Ensure filename is not empty
        if not base_filename:
            base_filename = 'file'

        company_title = getattr(
            instance.financial_asset.company, 'title', 'default-company')
        company_slug = self.persian_slugify(company_title)

        # Add unique ID to prevent collisions
        final_filename = f"{base_filename}.{ext}"

        # Combine the final path with the company folder
        return os.path.join(f"financial_analysis/diagnoses/files/{company_slug}", final_filename)

        # Add unique ID to prevent collisions
        final_filename = f"{base_filename}.{ext}"

        return os.path.join(self.path, final_filename)

    def generate_otp(self):
        """Generate a 6-digit OTP."""
        return str(np.random.randint(100000, 999999))

    def send_otp(self, phone_number, otp):
        """Send OTP to the given phone number (placeholder for SMS integration)."""
        # Here you should integrate with an SMS provider
        # For now, it's just printing the OTP as a placeholder
        print(f"Sending OTP {otp} to {phone_number}")

    def persian_slugify(self, value):
        """Slugify a string, keeping Persian characters and numbers."""
        # Keep Persian characters and numbers
        value = re.sub(r'[^\u0600-\u06FF0-9\s-]', '', value)
        value = re.sub(r'[\s]+', '-', value)  # Replace spaces with hyphens
        return value.strip('-')
