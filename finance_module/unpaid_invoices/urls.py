from django.urls import path, include
from django.views import generic

from . import views

app_name = "unpaid_invoices"

smart_table_urlpatterns = [
    path("", include(views.paid_invoices_smart_table)),
    path("", include(views.unpaid_invoices_smart_table)),
]
routers = [
    {"title": "", "icon": "", "pattern_name": "", "children": [
        {"title": "", "icon": "<i>...", "pattern_name": "",}
    ]},
    {"title": "", "icon": "", "pattern_name": "", "children": []},
    {"title": "", "icon": "", "pattern_name": "", "children": []},
    {"title": "", "icon": "", "pattern_name": "", "children": []},
    {"title": "", "icon": "", "pattern_name": "", "children": []},
    {"title": "", "icon": "", "pattern_name": "", "children": []},
]
urlpatterns = [
    path("", generic.RedirectView.as_view(pattern_name="finance_module:unpaid_invoices:import"), name="index"),
    path(
        "import",
        views.ImportTemplateView.as_view(),
        name="import",
    ),
    path(
        "list",
        views.ListTemplateView.as_view(),
        name="list",
    ),
    path(
        "unloading",
        views.UnloadingInvoicesPaidListView.as_view(),
        name="unloading_invoices_paid",
    ),
    path("paid-invoices", views.PaidInvoices.as_view(), name="paid_invoices"),
    path("pm-sum", views.PMSumTemplateView.as_view(), name="pm_sum"),
    path("update-pm-sum", views.update_pm_sum, name="update_pm_sum"),
    path("get-pm-sum", views.get_pm_sum, name="get_pm_sum"),
    path("mail-1c", views.mail_1c, ),
    path("smart-tables/", include(smart_table_urlpatterns))
]
