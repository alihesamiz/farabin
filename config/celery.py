from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
from django.conf import settings
from celery import Celery
import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')


app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'delete_expiered_otp': {
        'task': 'core.tasks.delete_expiered_otp',
        'schedule': crontab(minute='*/60'),
        'options': {'queue': 'default'},  
    }
}


app.conf.update(
    CELERY_QUEUES=settings.CELERY_QUEUES,
    # CELERY_ROUTES=settings.CELERY_ROUTES,
    CELERY_DEFAULT_QUEUE=settings.CELERY_DEFAULT_QUEUE,
    CELERY_DEFAULT_EXCHANGE='tasks',
    CELERY_DEFAULT_ROUTING_KEY='task.default',
)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
