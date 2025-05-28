from celery import shared_task
import logging

from django.contrib.auth import get_user_model
from django.utils import timezone


from apps.core.management.commands.database import Command
from apps.core.utils import GeneralUtils
from apps.core.models import OTP

User = get_user_model()
logger = logging.getLogger("core")


@shared_task(queue="high_priority")
def send_otp_task(user_id, phone_number):
    try:
        logger.info(
            f"Starting send_otp_task for user_id={user_id}, phone_number={phone_number}"
        )
        user = User.objects.get(id=user_id)
        otp = OTP(user=user)
        otp_code = otp.generate_otp()
        otp.otp_code = otp_code
        otp.save()
        util = GeneralUtils()
        util.send_otp(phone_number, otp_code)
        logger.info(f"OTP {otp_code} sent successfully to {phone_number}")

    except User.DoesNotExist:
        logger.error(f"Failed to send OTP: User with ID {user_id} does not exist")
    except Exception as e:
        logger.exception(f"Error occurred while sending OTP to {phone_number}: {e}")


@shared_task(bind=True)
def delete_expiered_otp(self):
    try:
        logger.info("Starting delete_expired_otp task")

        thirty_minutes_ago = timezone.now() - timezone.timedelta(minutes=30)
        otps = OTP.objects.filter(created_at__lt=thirty_minutes_ago)
        deleted_count, _ = otps.delete()
        logger.info(f"Deleted {deleted_count} expired OTPs")

    except Exception as e:
        logger.exception(f"Error occurred in delete_expired_otp: {e}")
        self.retry(exc=e, countdown=60, max_retries=3)


@shared_task(bind=True)
def backup_database(self, action="backup"):
    try:
        logger.info("Start Backup Database...")
        cmd = Command()
        cmd.handle(action=action)
        logger.info("Backup finished")
    except Exception as e:
        logger.exception(f"Error occurred in backup_database: {e}")
        self.retry(exc=e, countdown=60, max_retries=3)
