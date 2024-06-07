from django.urls import path
from .views import display_data, save_data, update_data, upload_data, update_pm, get_error, update_plan_month, export_to_excel, upload_google, delete_data, sum_itogi, new_test


urlpatterns = [
    path('display/', display_data, name='display_data'),
    path('display/save/', save_data, name='save_data'),
    path("update-data/", update_data, name="update_data"),
    path('upload-data/', upload_data, name='upload_data'),
    path('update-pm/', update_pm, name="update_pm"),
    path('get-error/', get_error, name='get_error' ),
    path('update_plan_month/', update_plan_month, name='update_plan_month'),
    path('export-data/', export_to_excel, name='export_data'),
    path('upload-google/', upload_google, name='upload_google'),
    path('delete-data/', delete_data, name='delete_data'),
    path('sum-itogi/', sum_itogi, name='sum_itogi'),

    path('test/', new_test, name='test')
]
