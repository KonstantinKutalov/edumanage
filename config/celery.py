from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Установка переменной окружения DJANGO_SETTINGS_MODULE, чтобы Celery знал, какие настройки Django использовать.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра Celery с именем проекта
app = Celery('config')

# Использование настроек Django в качестве настроек Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическая обнаружение и регистрация задач из приложений Django
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
