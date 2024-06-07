from django.urls import path
from . import views


urlpatterns = [
    path('transform-xlsx-file', views.TransformXLSXFileView.as_view(), name='transform-xlsx-file'),
]
