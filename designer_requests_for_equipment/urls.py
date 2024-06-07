from django.urls import path
from designer_requests_for_equipment import views as v

urlpatterns = [
    path("", v.main, name="designer_requests_for_equipment"),
    path("get-data-by-equip", v.get_data_by_equip, name="get_data_by_equip"),
    path("get-sub-data-by-id", v.get_sub_data_by_id, name="get_sub_data_by_id"),
    path("export-to-excel", v.export_to_excel, name="export_to_excel"),
    path('first-lvl-import', v.import_from_file, name='import_from_file'),
    path('junk-page', v.junk_page, name='junk_page'),
    path('import-constructor', v.import_consrtuctor, name="import_constructor"),
]

