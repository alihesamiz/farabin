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
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.broker_url = 'redis://redis:6379/0'
app.conf.result_backend = 'redis://redis:6379/0'

app.conf.beat_schedule = {
    'update_request_status': {
        'task': 'company.tasks.update_request_status',
        'schedule': crontab(minute='*/15'),
    }}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
