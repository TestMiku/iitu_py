from django.urls import path
from django.views.generic import RedirectView, TemplateView

from . import views

app_name = "mandatory_payments"
urlpatterns = [
    path("", RedirectView.as_view(pattern_name="finance_module:mandatory_payments:import_mandatory_payments", permanent=True), name="index"),
    path("import-mandatory-payments", views.ImportMandatoryPaymentsTemplateView.as_view(), name="import_mandatory_payments"),
    path("create-access-to-others-exception-for-project-manager", views.CreaetAccessToOthersExceptionForProjectManagerTemplateView.as_view(), name="create_access_to_others_exception_for_project_manager"),
    path("accrual-calculator", views.AccrualCalculatorTemplateView.as_view(), name="accrual_calculator"),
    path("seizure-list", TemplateView.as_view(template_name="finance_module/mandatory_payments/seizure_list.html"), name="seizure_list"),
    path("accrual-list", TemplateView.as_view(template_name="finance_module/mandatory_payments/accrual_list.html"), name="accrual_list"),
    path("list", views.ListTemplateView.as_view(), name="list"),
    path('unloading', views.UnloadingMandatoryPaymentsListView.as_view(), name='unloading_mandatory_payments'),
]
