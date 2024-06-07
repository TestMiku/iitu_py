from django.urls import path
from django.conf.urls.static import static
from . import views as v

urlpatterns = [
    # path("", main, name="deadline"),
    path("", v.main, name="deadline"),
    path("file-upload/", v.upload_file, name="file_upload"),
    path("search", v.search, name="search"),
    path("get-current-data", v.get_current_data, name="search"),
    path("get-all-data-by-id", v.all_data, name="all_data"),
    path("get-data-by-invoice", v.filtered_data_by_invoice, name="filtered_data_by_invoice"),
    path("get-all-projects", v.get_all_projects_from_data, name="get_all_projects_from_data"),
    path("get-all-project-managers", v.get_all_project_managers_from_data, name="get_all_project_managers_from_data"),
]
