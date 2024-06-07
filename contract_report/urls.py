from django.urls import path
from . import views
from . import scripts

urlpatterns = [
    # path("", views.ChoiceTemplateView.as_view()),
    path("", views.show_merged_data, name="process_excel"),
    path("import_esf_a77_data/", views.import_esf_a77_data, name="import_esf_a77_data"),
    path("import_supplier_data/", views.import_supplier_data, name="import_supplier_data"),
    path("merge_models/", views.merge_models, name="merge_models"),
    path("suppliers/", views.suppliers, name="suppliers"),
    path("create_supplier/", views.create_supplier, name="create_supplier"),
    path("delete_supplier/<int:supplier_id>/", views.delete_supplier, name="delete_supplier"),
]