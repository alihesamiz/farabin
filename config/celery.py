from __future__ import absolute_import, unicode_literals

import os

from celery import Celery  # type: ignore
from celery.schedules import crontab  # type: ignore
from django.conf import settings  # type: ignore

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

app = Celery("config")


app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "backup-database-every-sunday-and-wednesday-at-8pm": {
        "task": "core.tasks.backup_database",
        "schedule": crontab(hour=20, minute=0, day_of_week="0,3"),
        "options": {"queue": "high_priority"},
    },
}


app.conf.update(
    CELERY_QUEUES=settings.CELERY_QUEUES,
    # CELERY_ROUTES=settings.CELERY_ROUTES,
    CELERY_DEFAULT_QUEUE=settings.CELERY_DEFAULT_QUEUE,
    CELERY_DEFAULT_EXCHANGE="tasks",
    CELERY_DEFAULT_ROUTING_KEY="task.default",
)


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
