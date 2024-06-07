from django.urls import path
from .views import main, download_excel, download_html, delete_order, delete_all

app_name = 'constructor_do'

urlpatterns = [
    path("", main, name="constructor_do"),
    path("download-excel/", download_excel, name="download_excel"),
    path("download-html/", download_html, name="download_html"),
    path("delete-order/<str:index>", delete_order, name="delete_order"),
    path("delete-all", delete_all, name="delete_all"),
]
