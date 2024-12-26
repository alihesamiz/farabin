# project/celery.py
from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'update_request_status_task': {
        'task': 'company.tasks.update_request_status_task',
        'schedule': crontab(minute='*/30'),
    }}

app.conf.beat_schedule = {
    'delete_expiered_otp': {
        'task': 'core.tasks.delete_expiered_otp',
        'schedule': crontab(minute='*/60'),
    }}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
