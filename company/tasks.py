import requests
import json
from django.db.transaction import atomic
from celery import shared_task
from .models import Request
from ticket.models import Agent, Department
from django.contrib.auth import get_user_model


@shared_task
def update_request_status():
    for request in Request.objects.filter(status=Request.REQUEST_STATUS_NEW):
        request.check_and_update_status()


@shared_task
def send_file_uploading_notification(name):
    
    staff_users = get_user_model().objects.filter(is_staff=True)
    
    department = Department.objects.get(name='کارشناسی')
    
    agents = Agent.objects.filter(user__in=staff_users, department=department)

    # url = "https://api2.ippanel.com/api/v1/sms/pattern/normal/send"

    # headers = {
    #     'apikey': 'BXb2ovSeYtiAbfVT26gEb50Dmix_-nhAAQRp2v5yfXs=',
    #     'Content-Type': 'application/json'
    # }
    # file_name = "‌اظهارنامه‌ی" if name =='tax' else "‌ترازنامه‌ی"
    
    # with atomic():
    #     payload = json.dumps({
    #         "code": "",
    #         "sender": "+983000505",
    #         "recipient": [agents],
    #         "variable": {
    #             "message": f"{file_name} جدیدی بارگذاری شد" 
    #         }
    #     })

    #     response = requests.request(
    #         "POST", url, headers=headers, data=payload)
        # return response.text

