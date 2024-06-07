from django.urls import path
from .views import main, get_data_from_google_sheet, search_by_account_number, get_all_values_by_account_number

urlpatterns = [
    path("", main, name="import_maw"),
    path('search-by-account-number', search_by_account_number, name="search_by_account_number"),
    path("excel-fail-upload", get_data_from_google_sheet, name="excel_fail_upload"),
    path('get-all-values', get_all_values_by_account_number, name="get_all_values_by_account_number"),
    
]
