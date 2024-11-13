from celery import shared_task
from django.contrib.auth import get_user_model
from .models import OTP
from .utils import GeneralUtils

User = get_user_model()

@shared_task
def send_otp_task(user_id,phone_number):
    user = User.objects.get(id = user_id)
    otp = OTP(user=user)
    otp_code = otp.generate_otp()
    otp.otp_code = otp_code
    otp.save()
    util = GeneralUtils()
    util.send_otp(phone_number, otp_code)
    
    
#TODO: define a new sms sending 