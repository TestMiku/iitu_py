from django.urls import path
from .views import main, import_tcp, import_bs, download_template, hand_update, hand_update_1922, opened_accounts

urlpatterns = [
    path("", main, name="calculator_emr"),
    path("import-for-emr-tcp/", import_tcp, name="import_for_emr_tcp"),
    path("import-for-emr-bs/", import_bs, name="import_for_emr_bs"),
    path("download-temp/<str:filename>/", download_template, name="download_template"),
    path("bitrix-v/", main, name="bitrix_v"),
    path("hand-update/", hand_update, name="hand_update"),
    path("hand-update-1922/", hand_update_1922, name="hand_update_1912"),
    path("opened-accounts/<str:order_num>", opened_accounts, name="opened_accounts"),
    path("bitrix-v/opened-accounts/<str:order_num>", opened_accounts, name="bitrix_v/opened_accounts"),
]
