from django.urls import include, path
from django.views import generic

import api

from . import views

app_name = "for_treasurers"
smart_table_urlpatterns = [
    path("", include(views.mandatory_payment_seizures_smart_table)),
    path("", include(views.paid_invoices_smart_table)),
    path("", include(views.debt_translate_groups_smart_table)),
    path("", include(views.transfers_smart_table)),
    path("", include(views.sutochnye_smart_table)),
    path("", include(views.payment_confirmation_history_smart_table)),
    path("", include(views.administrative_transfers_smart_table)),
]
api_urlpatterns = [
    path("confirmation", views.confirmation),
    path("sutochnye/<int:pk>/mail-accountant", views.mail_accountant),
    path("sutochnye/<int:pk>/mail-000", views.mail_000)
]
urlpatterns = [
    path(
        "",
        generic.RedirectView.as_view(
            pattern_name="finance_module:for_treasurers:confirmation"
        ),
        name="index",
    ),
    path("confirmation", views.ConfirmationTemplateView.as_view(), name="confirmation"),
    path("smart-tables/", include(smart_table_urlpatterns)),
    path("api/", include(api_urlpatterns))
]
