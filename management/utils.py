from filelock import FileLock
import glob
import time
import os

from django.conf import settings

from rest_framework import (response, status)


def get_latest_file(company_name: str):
    """Find the most recent generated file for a company (to handle concurrent requests)."""

    folder = os.path.join(settings.MEDIA_ROOT, "organization_charts")
    pattern = os.path.join(folder, f"updated_{company_name}_*.xlsx")
    files = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
    return files[0] if files else None


def check_file_ready(company_name: str):
    """Check if the latest file exists and is fully written (handling async writes)."""
    latest_file = get_latest_file(company_name)
    if not latest_file:
        return response.Response({"error": "File not ready. Try again later."}, status=status.HTTP_404_NOT_FOUND)

    lock = FileLock(f"{latest_file}.lock")
    if lock.is_locked:
        return response.Response({"error": "File is being processed. Try again soon."}, status=status.HTTP_202_ACCEPTED)
    return latest_file


def get_updated_file_path(company_name: str):
    """Generate a unique filename using a timestamp to avoid overwriting in async environments."""
    timestamp = int(time.time())
    folder = os.path.join(settings.MEDIA_ROOT, "organization_charts")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, f"updated_{company_name}_{timestamp}.xlsx")

def get_file_field(field):
    """Returns the existing file based on the company given field

    Args:
        field (String): Companys' activity field

    Returns:
        String: Existing file field name
    """
    
    REVERSED_FILE_FIELDS = {field: key for key, fields in FILE_FIELDS.items() for field in fields}
    return REVERSED_FILE_FIELDS.get(field)


FILE_FIELDS ={
    "general": ["some_field","another field"],
}

