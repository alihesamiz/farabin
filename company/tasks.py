from celery import shared_task
from .models import Request

@shared_task
def update_request_status():
    for request in Request.objects.filter(status=Request.REQUEST_STATUS_NEW):
        request.check_and_update_status()