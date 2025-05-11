from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
from django.conf import settings
from celery import Celery
import os

from config.settings import development


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

app = Celery("config")


app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "delete_expiered_otp": {
        "task": "core.tasks.delete_expiered_otp",
        "schedule": crontab(minute="*/60"),
        "options": {"queue": "default"},
    }
}

app.conf.beat_schedule = {
    "backup-database-every-sunday-and-wednesday-at-8pm": {
        "task": "core.tasks.backup_database",
        "schedule": crontab(hour=20, minute=0, day_of_week="0,3"),
        "options": {"queue": "high_priority"},
    },
}


app.conf.update(
    CELERY_QUEUES=development.CELERY_QUEUES,
    # CELERY_ROUTES=development.CELERY_ROUTES,
    CELERY_DEFAULT_QUEUE=development.CELERY_DEFAULT_QUEUE,
    CELERY_DEFAULT_EXCHANGE="tasks",
    CELERY_DEFAULT_ROUTING_KEY="task.default",
)


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
