from django.urls import include, path
from rest_framework import routers
from api.views import UserListCreateView

from reporter import views

default_router = routers.DefaultRouter()
default_router.register("reports", views.ReportViewSet, "report")

app_name = "api"
urlpatterns = [
    path("", include(default_router.urls), name="root"),
    path("users/", UserListCreateView.as_view(), name='user-list-create'),
]
