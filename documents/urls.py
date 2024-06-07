from django.urls import path, reverse_lazy
from django.views import generic

from . import views

app_name = "documents"
urlpatterns = [
    path("", generic.RedirectView.as_view(url=reverse_lazy("documents:list"))),
    path("list", views.ChoiceTemplateView.as_view(), name="list"),
    path("create", views.ChoiceCreateView.as_view(), name="create"),
    path("<path:path>/create", views.ChoiceCreateView.as_view(), name="create_with_path"),
    path("<path:path>/update", views.ChoiceUpdateView.as_view(), name="update_with_path"),
    path("<path:path>/delete", views.ChoiceDeleteView.as_view(), name="delete_with_path"),
    path("<path:path>/list", views.ChoiceTemplateView.as_view(), name="list_with_path"),
]
