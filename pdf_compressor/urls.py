from django.urls import path

from . import views

app_name = "pdf_compressor"
urlpatterns = [
    path("", views.CompressFormView.as_view(), name="compress")
]
