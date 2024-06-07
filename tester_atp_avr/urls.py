from django.urls import path

from . import views

app_name = "tester-atp-avr"
urlpatterns = [
    path("", views.ATPAVRFormView.as_view(), name="atp-avr-form"),
    path("load-tcp", views.TCPFileForm.as_view(), name="load-tcp"),
    path("tcps", views.TCPFileList.as_view(), name="tcp-file-list"),
    path("get-tcp-categories", views.get_tcp_categories, name="get-tcp-categories"),
    path("get-tables-as-html", views.get_tables_as_html, name="get-tables-as-html"),
    path("get-tcps", views.get_tcps, name="get-tcps"),

    path("add-wt", views.add_wt),
    path("add-cnd", views.add_cnd),
    path("edit-wt/<int:pk>", views.edit_wt),
    path("edit-wt/del/<int:pk>", views.del_wt),
    path("edit-cnd/<int:pk>", views.edit_cnd),
    path("edit-cnd/del/<int:pk>", views.del_cnd),
    path("list-wt", views.list_wt, name="list-wt"),
    path("list-cnd", views.list_cnd, name="list-cnd"),

]
