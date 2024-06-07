import datetime

from django.urls import include, path, register_converter
from django.views.generic import RedirectView

from . import views


class DateConverter:
    regex = "\d+-\d+-\d+"

    def to_python(self, value: str) -> datetime.date:
        return datetime.datetime.strptime(value, "%Y-%m-%d").date()

    def to_url(self, value: datetime.date) -> str:
        return value.strftime("%Y-%m-%d")


register_converter(DateConverter, "date")

app_name = "division_of_financial_planning"

table_urlpatterns = [
    path("rows", views.rows),
    path("<date:date>/rows", views.rows),
    path("rows/<int:row_id>", views.row),
    path("<date:date>/rows/<int:row_id>", views.row),
    path("rows/<int:row_id>/cells", views.cells),
    path("<date:date>/rows/<int:row_id>/cells", views.cells),
]
api_urlpatterns = [
    path("accounts-table", views.get_accounts_table),
    path("project-regions", views.get_project_regions),
    path("unload-daily-table", views.unload_daily_table),
    path("daily-table", views.get_daily_table),
    path("confirmation", views.confirmation),
    path("tables/<str:table_name>/", include(table_urlpatterns)),

    path("create-administrative-transfer", views.create_administrative_transfer),
    path("create-raschetnye", views.create_raschetnye),
    path("create-transfers", views.create_transfers),
    path("mail-raschetnye", views.mail_raschetnye),
    path("pay-chsi", views.pay_chsi),
]

smart_table_urlpatterns = [
    path("", include(views.mandatory_payment_seizures_smart_table)),
    path("", include(views.administrative_transfers_smart_table)),
    path("", include(views.chsi_groups_smart_table)),
    path("", include(views.raschetnye_smart_table)),
    path("", include(views.transfers_smart_table)),
]

urlpatterns = [
    path(
        "",
        RedirectView.as_view(
            pattern_name="finance_module:division_of_financial_planning:confirmation"
        ),
        name="index",
    ),
    path("confirmation", views.ConfirmationTemplateView.as_view(), name="confirmation"),
    path(
        "monthly-payments",
        views.MonthlyPaymentsTemplateView.as_view(),
        name="monthly_payments",
    ),
    path(
        "transfers",
        views.TransfersTemplateView.as_view(),
        name="transfers",
    ),
    path("daily", views.DailyTemplateView.as_view(), name="daily"),
    path("api/", include(api_urlpatterns)),
    path("smart-tables/", include(smart_table_urlpatterns)),
]
