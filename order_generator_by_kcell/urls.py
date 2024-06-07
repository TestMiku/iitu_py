from django.urls import path

from .views import main, handle_uploaded_file, import_data, import_page

urlpatterns = [
    path("", main, name="order_generator_by_kcell"),
    path("excel-file-upload", handle_uploaded_file, name="excel_upload"),
    path("update-data", import_data, name="import_data"),
    path("import-page", import_page, name="import_page"),
]
