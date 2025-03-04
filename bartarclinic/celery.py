from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bartarclinic.settings')

app = Celery('bartarclinic')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-expired-reservations-every-minute': {
        'task': 'main_app.tasks.check_expired_reservations',
        'schedule': crontab(minute='*/1'),  
    },
}