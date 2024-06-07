from django.urls import path
from . import views

urlpatterns = [
    path("", views.show_merged_data, name="process_excel"),
]