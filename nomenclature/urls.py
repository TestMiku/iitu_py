from django.urls import path
from nomenclature import views


urlpatterns = [
    path('', views.ExcelGuideView.as_view(), name='excel_guide'),
]
