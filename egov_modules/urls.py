from django.urls import path
from . import views


urlpatterns = [
    path('', views.EgovCreateOrderView.as_view(), name='egov_create_order'),
]