import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_application.settings')

app = Celery('weather_application')
app.config_from_object('django.conf:settings')
app.conf.broker_url = 'redis://localhost:6379/0'
# Load task modules from all registered Django app configs.
app.autodiscover_tasks(settings.INSTALLED_APPS)


app.conf.beat_schedule = {
    'my-task': {
        'task': 'weather_page.tasks.periodic_task',
        'schedule': 30.0, #crontab(minute='*/1'),
                'args': (),
    }
}
