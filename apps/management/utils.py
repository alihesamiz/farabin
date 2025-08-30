from filelock import FileLock
import logging
import glob
import time
import os


from django.conf import settings

from rest_framework import response, status


from apps.company.models import TechField

 
logger = logging.getLogger("management")


def get_latest_file(company_name: str):
    """Find the most recent generated file for a company (to handle concurrent requests)."""

    folder = os.path.join(settings.MEDIA_ROOT, "organization_charts")
    pattern = os.path.join(folder, f"updated_{company_name}_*.xlsx")
    files = sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True)
    if files:
        logger.info(
            f"Found {len(files)} file(s) matching pattern for company {company_name}. Returning the most recent."
        )
        return files[0]
    else:
        logger.warning(
            f"No files found for company {company_name} with the pattern: {pattern}"
        )
        return None


def check_file_ready(company_name: str):
    """Check if the latest file exists and is fully written (handling async writes)."""
    latest_file = get_latest_file(company_name)
    if not latest_file:
        logger.error(f"File for company {company_name} not found or not ready.")
        return response.Response(
            {"error": "File not ready. Try again later."},
            status=status.HTTP_404_NOT_FOUND,
        )

    lock = FileLock(f"{latest_file}.lock")
    if lock.is_locked:
        logger.info(
            f"File for company {company_name} is currently being processed. Returning status 202."
        )
        return response.Response(
            {"error": "File is being processed. Try again soon."},
            status=status.HTTP_202_ACCEPTED,
        )

    logger.info(f"File for company {company_name} is ready for use: {latest_file}")
    return latest_file


def get_updated_file_path(company_name: str):
    """Generate a unique filename using a timestamp to avoid overwriting in async environments."""
    timestamp = int(time.time())
    folder = os.path.join(settings.MEDIA_ROOT, "organization_charts")
    os.makedirs(folder, exist_ok=True)
    new_file_path = os.path.join(folder, f"updated_{company_name}_{timestamp}.xlsx")
    logger.info(
        f"Generated unique file path for company {company_name}: {new_file_path}"
    )
    return new_file_path


def get_file_field(field):
    """Returns the existing file based on the company given field"""
    logger.info(f"Fetching file field for tech field: {field}")

    REVERSED_TECH_FIELDS = {
        field: key
        for key, fields in settings.HUMAN_RESOURCE_FILE_FIELDS.items()
        for field in [
            (
                sub_field
                if sub_field != "__all__"
                else list(TechField.objects.values_list("name", flat=True))
            )
            for sub_field in fields
        ][0]
    }

    file_field = REVERSED_TECH_FIELDS[str(field)]

    if file_field:
        logger.info(f"File field found for field {field}.")
    else:
        logger.warning(f"No file field found for {field}. Returning None.")
    return file_field
