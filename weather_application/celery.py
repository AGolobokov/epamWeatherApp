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

from weather_page.tasks import counter


app.conf.beat_schedule = {
    'my-task': {
                # Регистрируем задачу. Для этого в качестве значения ключа task
                # Указываем полный путь до созданного нами ранее таска(функции)
        'task': 'weather_page.tasks.endure_ten_seconds',
                 # Периодичность с которой мы будем запускать нашу задачу
                 # minute='*/5' - говор
        'schedule': 30.0, #crontab(minute='*/1'),
                # Аргументы которые будет принимать функция
                'args': (),
    }
}
