from django.urls import path, include
from json_to_excel import views as v

urlpatterns = [
    path("", v.main, name="main"),
    path("for-7-11-2", v.handle_7_11_2, name="for_7_11_2"),
]