"""Выглядит дерьмово!"""

from django.urls import include, path
from django.views.generic import RedirectView

from . import serializers, views

api_urlpatterns = [
    path("project-regions", views.get_project_regions, name="api_get_project_regions"),
    path("accounts", views.get_accounts, name="api_get_accounts"),
    path(
        "mandatory-payments-sums",
        views.get_mandatory_payments_sums,
    ),
    path("table-cell-colors", views.get_table_cell_colors),
    path(
        "mandatory-payments-paid",
        views.get_mandatory_payments_paid,
        name="api_get_mandatory_payments_paid",
    ),
    path("payment-confirmation", views.get_payment_confirmation),
    path(
        "project-region-mandatory-payments-paid",
        views.get_project_region_mandatory_payments_paid,
    ),
    path(
        "create-unpaid-invoice-exception",
        views.create_unpaid_invoice_exception,
        name="api_post_create_unpaid_invoice_exception",
    ),
    path(
        "delete-unpaid-invoice-exception",
        views.delete_unpaid_invoice_exception,
        name="api_post_delete_unpaid_invoice_exception",
    ),
    path(
        "unpaid-invoices-field-unique-values",
        views.get_unpaid_invoices_field_unique_values,
        name="api_get_get_unpaid_invoices_field_unique_values",
    ),
    path(
        "interdivisional-debts-data",
        views.get_interdivisional_debts_data,
        name="api_get_interdivisional_debts_data",
    ),
    path("all-accounts", views.get_all_accounts, name="get_all_accounts"),
    path("process-transactions", views.process_transactions),
    path(
        "all-project-regions",
        views.get_all_project_regions,
        name="get_all_project_regions",
    ),
    path(
        "project-region-accounts",
        views.get_project_region_accounts,
        name="get_project_region_accounts",
    ),
    path(
        "project-region-accounts-table",
        views.get_project_region_accounts_table,
        name="get_project_region_accounts_table",
    ),
    path(
        "complete-paid-invoices",
        views.complete_paid_invoices,
        name="complete_paid_invoices",
    ),
    path(
        "statement-reconciliation-saved-result",
        views.get_statement_reconciliation_saved_result,
        name="get_statement_reconciliation_saved_result",
    ),
    path(
        "statement-reconciliation-saved-results",
        views.get_statement_reconciliation_saved_results,
        name="get_statement_reconciliation_saved_results",
    ),
    path("setoff", views.setoff),
    path("subdivisions", views.get_subdivisions, name="get_subdivisions"),
]

app_name = "finance_module"
urlpatterns = [
    path("", RedirectView.as_view(pattern_name="finance_module:all"), name="index"),
    path(
        "all",
        views.AllTemplateView.as_view(),
        name="all",
    ),
    path(
        "import-inflows",
        views.ImportInflowsTemplateView.as_view(),
        name="import_inflows",
    ),
    path(
        "interdivisional-debts",
        RedirectView.as_view(
            pattern_name="finance_module:interdivisional_debts_import"
        ),
        name="interdivisional_debts",
    ),
    path(
        "interdivisional-debts/import",
        views.InterdivisionalDebtsImportTemplateView.as_view(),
        name="interdivisional_debts_import",
    ),
    path(
        "interdivisional-debts/table",
        views.InterdivisionalDebtsTableTemplateView.as_view(),
        name="interdivisional_debts_table",
    ),
    path(
        "get-mandatory-payment-accrual-calculator",
        views.get_mandatory_payment_accrual_calculator,
        name="get_mandatory_payment_accrual_calculator",
    ),
    path(
        "runner-and-cash-register/",
        views.runner_and_cash_register,
        name="runner_and_cash_register",
    ),
    path("upload_excel/", views.upload_excel, name="upload_excel"),
    path(
        "paid-invoices", views.PaidInvoicesTemplateView.as_view(), name="paid_invoices"
    ),
    path("lend-company", views.LendCompanyTemplateView.as_view(), name="lend_company"),
    path(
        "unload_debts",
        views.UnloadingInterDivisionalDebtsListView.as_view(),
        name="unload_debts",
    ),
    path(
        "get-account-available-for",
        views.get_account_available_for,
        name="get_account_available_for",
    ),
    path(
        "get-mandatory-payment-seizures",
        views.get_mandatory_payment_seizures,
        name="get_mandatory_payment_seizures",
    ),
    path(
        "get-unpaid-invoices",
        views.get_unpaid_invoices_filter,
        name="get_unpaid_invoices",
    ),
    path(
        "statement-reconciliation",
        views.StatementReconciliationTemplateView.as_view(),
        name="statement_reconciliation",
    ),
    path("income-71-p/", views.Income71P.as_view(), name="income-71-p"),
    path("income-71-p/download-excel/", views.get_excel_income_71P, name="income-71-p-download-excel"),
    path(
        "get-statement-reconciliation-result",
        views.get_statement_reconciliation_result,
        name="get_statement_reconciliation_result",
    ),
    path("api/", include(api_urlpatterns)),
    path(
        "api-get-model-unique-values",
        views.api_get_model_unique_values,
        name="api_get_model_unique_values",
    ),
    path("api-get-model-rows", views.api_get_model_rows, name="api_get_model_rows"),
    path("", include(views.mandatory_payment_seizures_smart_table)),
    path("", include(views.paid_invoices_smart_table)),
    path("", include(views.unload_paid_invoices_smart_table)),
    path("", include(views.interdivisional_debts_smart_table)),
    path("", include(views.pm_sum_unpaid_invoices_smart_table)),
    path("", include(views.all_unpaid_invoices_smart_table)),
    path("", include(views.inflows_smart_table)),
    path("", include(views.daily_mandatory_payment_seizure_smart_table)),
    path("", include(views.debts_smart_table)),
    path("", include(views.sutochnye_smart_table)),
    path("unload", views.unload, name="unload"),
    path(
        "for-treasurers/",
        include("finance_module.for_treasurers.urls", namespace="for_treasurers"),
    ),
    path(
        "mandatory-payments/",
        include(
            "finance_module.mandatory_payments.urls", namespace="mandatory_payments"
        ),
    ),
    path(
        "division-of-financial-planning/",
        include(
            "finance_module.division_of_financial_planning.urls",
            namespace="division_of_financial_planning",
        ),
    ),
    path(
        "unpaid-invoices/",
        include("finance_module.unpaid_invoices.urls", namespace="unpaid_invoices"),
    ),
    path("create-sutochnye", views.create_sutochnye, name="create_sutochnye"),
]
