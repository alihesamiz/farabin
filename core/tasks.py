from celery import shared_task
from django.contrib.auth import get_user_model
from .models import OTP
from .utils import GeneralUtils
from django.utils import timezone

User = get_user_model()


@shared_task(queue='high_priority')
def send_otp_task(user_id, phone_number):
    user = User.objects.get(id=user_id)
    otp = OTP(user=user)
    otp_code = otp.generate_otp()
    otp.otp_code = otp_code
    otp.save()
    util = GeneralUtils()
    util.send_otp(phone_number, otp_code)


@shared_task(bind=True)
def delete_expiered_otp(self):
    try:
        
        thirty_minutes_ago = timezone.now() - timezone.timedelta(minutes=30)

        otps = OTP.objects.filter(created_at__lt=thirty_minutes_ago)
        otps.delete()

    except Exception as e:
        # Retry the task in case of an exception
        self.retry(exc=e, countdown=60, max_retries=3)

# TODO: define a new sms sending
