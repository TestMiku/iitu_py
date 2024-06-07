from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="document_debts"),
    path("docs", views.docs, name="document_debts_docs"),
    path("docs/<int:filter_id>", views.docs, name="document_debts_docs"),
    path("pbi/19_20", views.pbi_19_20, name="pbi_19_20"),
    path("pbi/filters", views.pbi_filters, name="pbi_filters"),
    path("<int:filter_id>", views.index, name="permanent_filter"),
]
