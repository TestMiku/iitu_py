from django.urls import path

from . import views

app_name = "order_entry_as_html"
urlpatterns = [
    path("", views.OrderEntryFormView.as_view(), name="form"),
    path(
        "html-kartel-convert/", views.convert_kar_tel_html, name="html-kartel-convert"
    ),
]
