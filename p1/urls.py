from django.urls import path, include

from main import views as main_views

urlpatterns = [
    path("", main_views.main_tables, name="home"),
    path("tester-atp-avr/", include("tester_atp_avr.urls")),
    path("documents/", include("documents.urls")),
    path("pdf_compressor/", include("pdf_compressor.urls")),
    path("reporter/", include("reporter.urls")),
    path("order-entry-as-html/", include("order_entry_as_html.urls")),
    path("finance-module/", include("finance_module.urls")),
]
