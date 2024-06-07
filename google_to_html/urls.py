# myapp/urls.py

from django.urls import path
from .views import index, googtogtml

urlpatterns = [
    path('', index, name='index'),
    path('googtogtml/', googtogtml, name='googtogtml'),

]
