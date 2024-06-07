from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установите переменную окружения 'DJANGO_SETTINGS_MODULE'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_avh.settings')

# Создайте экземпляр Celery и укажите имя проекта
app = Celery('portal_avh',
            broker='redis://localhost:6379' #'pyamqp://guest:guest@localhost:5672//',
            )

# Загрузите конфигурацию Celery из настроек Django
app.config_from_object('django.conf:settings', namespace='CELERY')
# Автоматически обнаруживайте и регистрируйте задачи из приложений Django
app.autodiscover_tasks()
