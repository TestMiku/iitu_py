from django.urls import path

from . import views

app_name = "reporter"
urlpatterns = [
    path("list", views.ReportListView.as_view(), name="list"),
    path("powerbi", views.powerbi, name="powerbi"),
    path("chart", views.chart_page, name="chart"),
    path('chart/get-chiced-value/', views.search_by_process, name="search_by_process"),
]
