from django.urls import path
from .views import notification_list, mark_as_read, latest_notifications

app_name = 'notifications'

urlpatterns = [
    path('', notification_list, name='list'),
    path('latest/', latest_notifications, name='latest'),
    path('mark-as-read/', mark_as_read, name='mark_as_read'),
]