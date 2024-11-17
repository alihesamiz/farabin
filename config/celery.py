# project/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
# Ensure 'company.tasks' is included
app.autodiscover_tasks(lambda: ['company.tasks'])
app.conf.broker_url='redis://redis:6379/0'
app.conf.result_backend='redis://redis:6379/0'

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
