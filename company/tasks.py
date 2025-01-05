import requests
import json
from django.db.transaction import atomic
from django.utils import timezone
from celery import shared_task
from .models import BaseRequest, DiagnosticRequest
from ticket.models import Agent, Department
from django.contrib.auth import get_user_model


# @shared_task
# def update_request_status():
#     all_requests=BaseRequest.objects.filter(status=BaseRequest.REQUEST_STATUS_NEW)
#     for request in all_requests:
#         request.check_and_update_status()


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


@shared_task(bind=True)
def update_request_status_task(self):
    try:
        # Calculate the time threshold
        fifteen_minutes_ago = timezone.now() - timezone.timedelta(minutes=15)

        # Update the status of relevant requests
        DiagnosticRequest.objects.filter(
            status=DiagnosticRequest.REQUEST_STATUS_NEW,
            created_at__lte=fifteen_minutes_ago
        ).update(status=DiagnosticRequest.REQUEST_STATUS_PENDING)

    except Exception as e:
        # Retry the task in case of an exception
        self.retry(exc=e, countdown=60, max_retries=3)
