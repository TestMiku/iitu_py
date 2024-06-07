import collections.abc
import datetime
import decimal
import functools
import json
import operator
import os
import re
from typing import Any

import pandas as pd
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import FieldError
from django.db import connection, transaction
from django.db.models import (
    Case,
    Q,
    QuerySet,
    Value,
    When,
)
from django.db.models.functions import Concat
from django.http import FileResponse, Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View, generic
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_POST
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from finance_module.services import (
    common_service,
    interdivisional_debts_service,
    mandatory_payments_service,
    smart_table_service,
    unload_logistic_service,
    unload_service,
    unpaid_invoices_service,
)
from main.models import AvhUser

from . import models, serializers, services
from .models import MandatoryPaymentAccrualCalculator, ProjectRegion, Runner
from .services import income_71P, statement_reconciliation_service


class AllTemplateView(LoginRequiredMixin, generic.TemplateView):
    template_name = "finance_module/all.html"


class LendCompanyTemplateView(generic.TemplateView):
    template_name = "finance_module/interdivisional_debts/lend_company.html"

    def post(self, request: HttpRequest) -> HttpResponse:
        sum_ = decimal.Decimal(request.POST.get("sum"))
        percent = decimal.Decimal(request.POST.get("percent"))
        project_region_id = request.POST.get("project-region-id")
        project_region = models.ProjectRegion.objects.get(id=project_region_id)
        to_account_id = request.POST.get("to-account-id")
        to_account = models.Account.objects.get(id=to_account_id)
        administrative_account = common_service.get_administrative_account()
        account_balance = common_service.get_account_balance(administrative_account)
        sum_with_percent = sum_ * (1 + percent / 100)
        assert sum_with_percent < account_balance
        debt_translate_group = models.DebtTranslateGroup(
            from_account=administrative_account,
            from_whom="Долги АДМ фактические",
            to_whom=project_region.name,
            to_account=to_account,
            sum=sum_with_percent,
            responsible=request.user,
            type="plus_minus",
        )
        models.Debt.objects.create(
            from_whom="Долги АДМ фактические",
            to_whom=project_region.name,
            sum=sum_with_percent,
            responsible=request.user,
            debt_translate_group=debt_translate_group,
            additional_properties={"sum": float(sum_), "percent": float(percent)},
        )
        return self.get(request)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        administrative_account = common_service.get_administrative_account()
        return super().get_context_data(
            administrative_account=administrative_account,
            administrative_account_balance=common_service.get_account_balance(
                administrative_account
            ),
            project_regions=models.ProjectRegion.objects.all(),
            loans_out=models.Debt.objects.exclude(
                additional_properties__isnull=True
            ).filter(from_whom="Долги АДМ фактические"),
            **kwargs,
        )


def get_all_accounts(request: HttpRequest) -> JsonResponse:
    return JsonResponse(
        {
            "accounts": serializers.AccountSerializer(
                models.Account.objects.all(), many=True
            ).data
        }
    )


@api_view(["POST"])
def get_unpaid_invoices_filter(request: Request) -> Response:
    paginator = PageNumberPagination()
    paginator.page_size = 30
    unpaid_invoices = models.UnpaidInvoice.objects.all()
    json_ = request.data
    filters = {}
    for key, value in json_.items():
        filters[f"{key}__in"] = value
    unpaid_invoices = unpaid_invoices.filter(**filters)
    result_page = paginator.paginate_queryset(unpaid_invoices, request)
    response = paginator.get_paginated_response(
        serializers.UnpaidInvoiceSerializer(result_page, many=True).data
    )
    return response


class ImportInflowsTemplateView(generic.TemplateView):
    template_name = "finance_module/import_inflows.html"

    def post(self, request: HttpRequest, *args, **kwargs):
        post_type = request.POST.get("post-type")
        if post_type == "import-inflows-7":
            uploaded_file = request.FILES.get("file")
            date = request.POST.get("date")
            assert uploaded_file is not None
            services.import_inflows_7(
                uploaded_file.file,
                date=datetime.datetime.strptime(date, "%Y-%m-%d").date()
                if date
                else None,
            )
        elif post_type == "import-inflows-71":
            date = request.POST.get("date")
            file1 = request.FILES.get("file1")
            file2 = request.FILES.get("file2")
            file1_name = file1.name
            data, file_path = income_71P.compare_files(file1, file2, file1_name)
        else:
            raise Http404()
        return self.get(request)


class InterdivisionalDebtsTableTemplateView(generic.TemplateView):
    template_name = "finance_module/interdivisional_debts/table.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        participants = sorted(interdivisional_debts_service.get_participants())
        rows = []
        for participant1 in participants:
            sums = []
            for participant2 in participants:
                if participant1 == participant2:
                    sums.append(0)
                    continue
                sums.append(
                    interdivisional_debts_service.get_debt_sum(
                        from_whom=participant1, to_whom=participant2
                    )
                )
            rows.append((participant1, sums))
        return super().get_context_data(
            participants=participants,
            rows=rows,
            **kwargs,
        )


class InterdivisionalDebtsImportTemplateView(generic.TemplateView):
    template_name = "finance_module/interdivisional_debts/import.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return super().get_context_data(**kwargs)

    def post(self, request: HttpRequest) -> HttpResponse:
        post_type = request.POST.get("post-type")
        if post_type == "import-debts":
            file = request.FILES["file"].file
            interdivisional_debts_service.import_debts(bytes_io=file)
        elif post_type == "update-debts":
            file = request.FILES.get("file")
            credits_sum = request.POST.get("credits-sum")
            if credits_sum:
                credits_sum = decimal.Decimal(credits_sum)
            interdivisional_debts_service.update_debts(
                bytes_io=file and file.file, credits_sum=credits_sum
            )
        elif post_type == "import-renewable-debts":
            file = request.FILES["file"].file
            interdivisional_debts_service.import_renewable_debts(bytes_io=file)
        else:
            raise Http404
        return self.get(request)


class UnloadingInterDivisionalDebtsListView(generic.ListView):
    template_name = "finance_module/interdivisional_debts/unload_debts.html"

    def get_queryset(self):
        return models.Debt.objects.all()

    def get(self, request, *args, **kwargs):
        if request.GET.get("file") == "":
            file = interdivisional_debts_service.unload_debts()
            return FileResponse(file, filename="unloading_debts.xlsx")

        return super().get(request, *args, **kwargs)


class PaidInvoicesTemplateView(generic.TemplateView):
    template_name = "finance_module/paid_invoices.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        today = timezone.localdate()
        paid_invoice_list = models.PaidInvoice.objects.filter(
            at__year=today.year, at__month=today.month, at__day=today.day
        )
        return super().get_context_data(paid_invoice_list=paid_invoice_list, **kwargs)


class StatementReconciliationTemplateView(generic.TemplateView):
    template_name = "finance_module/statement_reconciliation.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return super().get_context_data(
            variables=statement_reconciliation_service.get_variables(), **kwargs
        )


class Income71P(View):
    template_name = "finance_module/income-71P.html"
    # template_name = "finance_module/notifications.html"
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        file1 = request.FILES.getlist('file1[]')
        file2 = request.FILES.get("file2")

        data, file_path = income_71P.compare_files(file1, file2)
        if isinstance(data, JsonResponse):
            return data
        else:
            request.session["excel_path"] = file_path
            context = {"data": data}
            return render(request, self.template_name, context)


def get_excel_income_71P(request):
    try:
        file_path = request.session.get("excel_path")
        if not file_path or not os.path.exists(file_path):
            return HttpResponse("Файл не найден.", status=404)

        with open(file_path, "rb") as fh:
            response = HttpResponse(
                fh.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = "inline; filename=" + os.path.basename(
                file_path
            )
            return response
    except Exception as e:
        return HttpResponse(f"Ошибка обработки файлов: {e}", status=500)


def get_statement_reconciliation_result(request: HttpRequest) -> HttpResponse:
    uploaded_files = request.FILES.getlist("files")
    worksheet_name = request.POST.get("worksheet-name")
    start_row = request.POST.get("start-row")
    if start_row:
        start_row = int(start_row)
    date = datetime.datetime.strptime(request.POST.get("date"), "%Y-%m-%d").date()
    paid_invoices_file = request.FILES.get("paid-invoices-file")
    correspondents_map = request.POST.get("correspondents-map")
    exclude_from_exceptions = request.POST.get("exclude-from-exceptions")
    accounts_map = request.POST.get("accounts-map")
    variables = statement_reconciliation_service.get_variables()
    variables.correspondents_map = correspondents_map
    variables.accounts_map = accounts_map
    variables.exclude_from_exceptions = exclude_from_exceptions
    variables.save()
    try:
        result = statement_reconciliation_service.statement_reconciliation(
            uploaded_files=uploaded_files,
            date=date,
            paid_invoices_file=paid_invoices_file,
            worksheet_name=worksheet_name,
            start_row=start_row,
        ).tojson()
    except (
        statement_reconciliation_service.StatementReconciliationError
    ) as statement_reconciliation_error:
        return JsonResponse({"detail": str(statement_reconciliation_error)}, status=400)

    models.StatementReconciliationResult.objects.update_or_create(
        created_date=timezone.localdate(), date=date, defaults={"result": result}
    )
    return JsonResponse(result)


@api_view(["GET"])
def get_statement_reconciliation_saved_result(request: Request) -> Response:
    id = request.query_params.get("id")
    try:
        result = models.StatementReconciliationResult.objects.get(id=id)
    except models.StatementReconciliationResult.DoesNotExist:
        return Response({"detail": "Does not exist"}, status=404)
    return Response(result.result)


@api_view(["GET"])
def get_statement_reconciliation_saved_results(request: Request) -> Response:
    return Response(
        serializers.StatementReconciliationResultSerializer(
            models.StatementReconciliationResult.objects.all(), many=True
        ).data
    )


@api_view(["POST"])
def complete_paid_invoices(request: Request) -> Response:
    not_found_paid_invoices = []
    paid_invoices = []
    compele_count = 0
    reject_count = 0
    real_completed_count = 0
    real_rejected_count = 0
    today = timezone.localdate()
    for id_ in request.data.getlist("paid-invoice-id"):
        commission = request.data.get(f"paid-invoice-commission-{id_}")
        complete = request.data.get(f"paid-invoice-complete-{id_}") == "on"
        if complete:
            compele_count += 1
        else:
            reject_count += 1
        try:
            paid_invoice = models.PaidInvoice.objects.get(id=id_)
        except models.PaidInvoice.DoesNotExist:
            not_found_paid_invoices.append(id_)
            continue
        paid_invoices.append(paid_invoice.number)
        paid_invoice.commission = commission
        paid_invoice.commission_date = today
        if complete:
            real_completed_count += 1
            paid_invoice.complete(responsible=request.user)
        else:
            real_rejected_count += 1
            paid_invoice.reject(responsible=request.user)
    return Response(
        {
            "notFoundPaidInvoices": not_found_paid_invoices,
            "paidInvoices": paid_invoices,
            "completeCount": compele_count,
            "rejectCount": reject_count,
            "realCompletedCount": real_completed_count,
            "realRejectedCount": real_rejected_count,
        }
    )


@csrf_exempt
def api_get_model_unique_values(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    model = data["model"]
    field = data["field"]
    field_unique_values = data["fieldUniqueValues"]

    objects = getattr(models, model).objects.all()
    for field_, unique_values in field_unique_values.items():
        if "exclude" in unique_values:
            objects = objects.exclude(**{f"{field_}__in": unique_values["exclude"]})
        else:
            objects = objects.filter(**{f"{field_}__in": unique_values["include"]})
    filtered_unique_values = list(objects.values_list(field, flat=True).distinct())
    objects = getattr(models, model).objects.all()
    return JsonResponse(
        {
            "uniqueValues": [
                {
                    "uniqueValue": unique_value,
                    "checked": unique_value in filtered_unique_values,
                }
                for unique_value in objects.values_list(field, flat=True).distinct()
            ]
        }
    )


@csrf_exempt
def api_get_model_rows(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    model = data["model"]
    field_unique_values = data["fieldUniqueValues"]
    objects = getattr(models, model).objects.all()

    for field, unique_values in field_unique_values.items():
        if "exclude" in unique_values:
            objects = objects.exclude(Q(**{f"{field}__in": unique_values["exclude"]}))
        else:
            objects = objects.filter(Q(**{f"{field}__in": unique_values["include"]}))
    return JsonResponse({"rows": list(objects.values())})


@smart_table_service.smart_table(
    "mandatory-payment-seizure",
    models.MandatoryPaymentSeizure,
    serializers.MandatoryPaymentSeizureSerializer,
)
def mandatory_payment_seizures_smart_table(
    request: HttpRequest, queryset: QuerySet, field: str | None = None
) -> QuerySet:
    return queryset.exclude(imported_from_file=True).filter(
        project_region__in=common_service.get_project_regions(
            user=request.user if request.user.is_authenticated else None
        )
    )


@smart_table_service.smart_table(
    "paid-invoices", models.PaidInvoice, serializers.PaidInvoiceSerializer
)
def paid_invoices_smart_table(
    request: HttpRequest, queryset: QuerySet, field: str | None = None
) -> QuerySet:
    return queryset.filter(
        project_region__in=common_service.get_project_regions(
            user=request.user if request.user.is_authenticated else None
        )
    )


@smart_table_service.smart_table(
    "interdivisional-debts",
    models.DebtTranslateGroup,
    serializers.DebtTranslateGroupSerializer,
)
def interdivisional_debts_smart_table(
    request: HttpRequest, queryset: QuerySet, field: str | None = None
) -> QuerySet:
    return queryset.filter(
        from_whom__in=common_service.get_project_regions(
            user=request.user if request.user.is_authenticated else None
        )
        .values_list("name", flat=True)
        .distinct()
    )


@smart_table_service.smart_table(
    "debts",
    models.Debt,
    serializers.DebtSerializer,
)
def debts_smart_table(
    request: HttpRequest, queryset: QuerySet, field: str | None = None
) -> QuerySet:
    return queryset.exclude(imported_from_file=True).filter(
        from_whom__in=common_service.get_project_regions(
            user=request.user if request.user.is_authenticated else None
        )
        .values_list("name", flat=True)
        .distinct()
    )


@smart_table_service.smart_table(
    "sutochnye",
    models.Sutochnye,
    serializers.SutochnyeSerializer,
)
def sutochnye_smart_table(
    request: HttpRequest, queryset: QuerySet, field: str | None = None
) -> QuerySet:
    return queryset.filter(
        project_region__in=common_service.get_project_regions(
            user=request.user if request.user.is_authenticated else None
        )
    )


@smart_table_service.smart_table(
    "pm-sum-unpaid-invoices", models.UnpaidInvoice, serializers.UnpaidInvoiceSerializer
)
def pm_sum_unpaid_invoices_smart_table(
    request: HttpRequest, queryset: QuerySet, field: str | None = None
) -> QuerySet:
    if not request.user.is_superuser:
        queryset = queryset.filter(
            approver__startswith=request.user.avh_user_id_from_email
        )
    return unpaid_invoices_service.annotate_unpaid_invoices(queryset)


@smart_table_service.smart_table(
    "all-unpaid-invoices", models.UnpaidInvoice, serializers.UnpaidInvoiceSerializer
)
def all_unpaid_invoices_smart_table(
    request: HttpRequest, queryset: QuerySet, field: str | None = None
) -> QuerySet:
    if not request.user.is_superuser:
        project_regions = common_service.get_project_regions(user=request.user)
        filter_ = functools.reduce(
            lambda x, y: (
                x | Q(approver__startswith=y) if x else Q(approver__startswith=y)
            ),
            (
                project_region.project_manager.avh_user_id_from_email
                for project_region in project_regions
                if project_region.project_manager
            ),
            None,
        )
        if filter_:
            queryset = queryset.filter(filter_)
    return unpaid_invoices_service.annotate_unpaid_invoices(queryset)


@smart_table_service.smart_table("inflows", models.Inflow, serializers.InflowSerializer)
def inflows_smart_table(
    request: HttpRequest, queryset: QuerySet, field: str | None = None
) -> QuerySet:
    return queryset


@smart_table_service.smart_table(
    "daily-mandatory-payment-seizure",
    models.MandatoryPaymentSeizure,
    serializers.MandatoryPaymentSeizureSerializer,
)
def daily_mandatory_payment_seizure_smart_table(
    request: HttpRequest, queryset: QuerySet, field: str | None = None
) -> QuerySet:
    return queryset.annotate(
        responsible_fullname=Case(
            When(
                responsible__isnull=False,
                then=Concat(
                    "responsible__first_name", Value(" "), "responsible__last_name"
                ),
            ),
        )
    ).exclude(
        Q(
            status__in=[
                models.rejected_mandatory_payment_seizure_status(),
                models.default_mandatory_payment_seizure_status(),
            ]
        )
        | Q(imported_from_file=True)
    )


@csrf_exempt
def get_mandatory_payment_accrual_calculator(request: HttpRequest) -> HttpResponse:
    id = request.GET.get("id")
    if not id:
        return JsonResponse(
            {"detail": '"id" should be set in query parameters'}, status=400
        )
    try:
        mandatory_payments_accrual_calculator = (
            MandatoryPaymentAccrualCalculator.objects.get(id=id)
        )
    except MandatoryPaymentAccrualCalculator.DoesNotExist:
        return JsonResponse({"detail": "Not found"}, status=404)
    return JsonResponse(
        serializers.MandatoryPaymentAccrualCalculatorSerializer(
            mandatory_payments_accrual_calculator
        ).data
    )


@csrf_exempt
def get_mandatory_payment_seizures(request: HttpRequest) -> JsonResponse:
    queryset = models.MandatoryPaymentSeizure.objects.filter(
        status__name=models.COMPLETED_MANDATORY_PAYMENT_SEIZURE_STATUS_NAME
    )
    date_filter_type = request.GET.get("date-filter-type")
    today = timezone.localdate()

    if date_filter_type == "today":
        queryset = queryset.filter(
            datetime__year=today.year,
            datetime__month=today.month,
            datetime__day=today.day,
        )
    elif date_filter_type == "range":
        start = request.GET.get("start-date")
        if start:
            queryset = queryset.filter(datetime__gte=start)
        end = request.GET.get("end-date")
        if end:
            end = datetime.datetime.strptime(end, "%Y-%m-%d")
            queryset = queryset.filter(
                datetime__year__lte=end.year,
                datetime__month__lte=end.month,
                datetime__day__lte=end.day,
            )
    elif date_filter_type == "last-month":
        queryset = queryset.filter(
            datetime__year=today.year, datetime__month=today.month
        )

    return JsonResponse(
        serializers.MandatoryPaymentSeizureSerializer(queryset, many=True).data,
        safe=False,
    )


def get_mandatory_payments_paid(request: HttpRequest) -> JsonResponse:
    return JsonResponse(
        {
            "mandatory_payments_paid": common_service.mandatory_payments_paid(
                request.user
            )
        }
    )


@permission_classes([IsAuthenticated])
@api_view(["GET"])
def get_project_region_mandatory_payments_paid(request: Request) -> Response:
    return Response(
        common_service.get_project_region_mandatory_payments_paid(request.user)
    )


@require_POST
def get_unpaid_invoices_field_unique_values(request: HttpRequest) -> JsonResponse:
    field = request.GET.get("field")
    if not field:
        return JsonResponse({"detail": "field required in query params"})
    try:
        filters = {}
        json_ = json.loads(request.body)
        for key, value in json_.items():
            if key == field:
                continue
            filters[f"{key}__in"] = value
        return JsonResponse(
            {
                "unique_values": list(
                    models.UnpaidInvoice.objects.filter(**filters)
                    .values_list(field, flat=True)
                    .distinct()
                )
            }
        )
    except FieldError:
        return JsonResponse({"detail": f"{field} does not exists"}, status=404)


@csrf_exempt
@require_POST
def create_unpaid_invoice_exception(request: HttpRequest) -> JsonResponse:
    number = request.GET.get("number")
    if not id:
        return JsonResponse({"detail": "number required"}, status=400)

    try:
        unpaid_invoice = models.UnpaidInvoice.objects.get(number=number)
    except models.UnpaidInvoice.DoesNotExist:
        return JsonResponse(
            {"detail": f"UnpaidUnvoice with number {number} does not exists"},
            status=404,
        )

    _, created = unpaid_invoice.create_exception(
        request.user if request.user.is_authenticated else None
    )

    return JsonResponse({"detail": "Created"}, status=201 if created else 200)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_unpaid_invoice_exception(request: HttpRequest) -> JsonResponse:
    number = request.GET.get("number")
    if not number:
        return JsonResponse({"detail": "number required"}, status=400)

    try:
        unpaid_invoice = models.UnpaidInvoice.objects.get(number=number)
    except models.UnpaidInvoice.DoesNotExist:
        return JsonResponse(
            {"detail": f"UnpaidUnvoice with number {number} does not exists"},
            status=404,
        )

    unpaid_invoice.delete_today_exceptions()
    return JsonResponse({"detail": "Deleted"})


def get_all_project_regions(request: HttpRequest) -> JsonResponse:
    return JsonResponse(
        {
            "project_regions": serializers.ProjectRegionSerializer(
                models.ProjectRegion.objects.all(), many=True
            ).data
        }
    )


@csrf_exempt
def load_debts_between_project_managers_file(request: HttpRequest) -> HttpResponse:
    debts_between_project_managers_file = request.FILES[
        "debts-between-project-managers-file"
    ]
    loader = services.Loader()
    try:
        loader.load_bytes_io(debts_between_project_managers_file.file)
    except Exception as error:
        return JsonResponse({"detail": str(error)}, status=400)
    return JsonResponse(loader.data, headers={"Cache-Control": "max-age=3600"})


def get_account_available_for(request: HttpRequest) -> JsonResponse:
    id = request.GET.get("id")
    if not id:
        return JsonResponse(
            {"detail": "id must be set in query parameters"}, status=400
        )

    try:
        account = models.Account.objects.get(id=id)
    except models.Account.DoesNotExist:
        return JsonResponse(
            {"detail": f"Account does not exists with id {id}"}, status=404
        )

    return JsonResponse(
        serializers.ProjectRegionSerializer(
            account.available_for.all(), many=True
        ).data,
        safe=False,
    )


@transaction.atomic
@require_POST
@login_required
def create_sutochnye(request: HttpRequest) -> JsonResponse:
    try:
        sutochnye = models.Sutochnye.objects.create(
            project_region=models.ProjectRegion.objects.get(
                id=request.POST.get("project-region-id")
            ),
            account=models.Account.objects.get(id=request.POST.get("account-id")),
            name=request.POST.get("name"),
            days=request.POST.get("days"),
            sum=request.POST.get("sum"),
            subdivision=models.Subdivision.objects.get(
                id=request.POST.get("subdivision-id")
            ),
            project=request.POST.get("project"),
            responsible=request.POST.get("responsible"),
            business_trip_start_date=request.POST.get("business-trip-start-date"),
            business_trip_end_date=request.POST.get("business-trip-end-date"),
            destination_point=request.POST.get("destination-point"),
        )
    except models.ProjectRegion.DoesNotExist:
        return JsonResponse({"detail": "Project region does not exists"}, status=404)
    except models.Account.DoesNotExist:
        return JsonResponse({"detail": "Account does not exists"}, status=404)
    except models.Subdivision.DoesNotExist:
        return JsonResponse({"detail": "Subdivision does not exists"}, status=404)
    except Exception as exception:
        return JsonResponse({"detail": str(exception)}, status=400)
    files = []
    for file in request.FILES.getlist("files"):
        files.append(models.SutochnyeFile(sutochnye=sutochnye, file=file))
    models.SutochnyeFile.objects.bulk_create(files)
    return JsonResponse({"id": sutochnye.id}, status=201)


@transaction.atomic
@require_POST
@login_required
def process_transactions(request: HttpRequest) -> JsonResponse:
    """
    #TODO: Сделать проверку на баланс в расчётным счету
    """
    data = json.loads(request.body)
    try:
        mandatory_payment_seizures: list[models.MandatoryPaymentSeizure] = []
        for project_region_id, mandatory_payment_datas in data[
            "projectRegionMandatoryPayments"
        ].items():
            project_region = models.ProjectRegion.objects.get(id=project_region_id)
            try:
                account_id = next(
                    (
                        account_data["id"]
                        for account_data in data["selectedAccounts"][
                            "mandatory-payments"
                        ]
                        if int(account_data["projectRegionId"])
                        == int(project_region_id)
                    ),
                    None,
                )
            except KeyError:
                assert False, "р/с"
            assert account_id is not None, "р/с"
            account = models.Account.objects.get(id=account_id)
            for mandatory_payment_data in mandatory_payment_datas:
                sum_ = decimal.Decimal(mandatory_payment_data["sum"])
                assert sum_ > 0, "the sum cannot be less than or equal to zero"
                mandatory_payment = models.MandatoryPayment.objects.get(
                    id=mandatory_payment_data["mandatoryPaymentId"]
                )
                mandatory_payment_seizures.append(
                    models.MandatoryPaymentSeizure(
                        project_region=project_region,
                        mandatory_payment=mandatory_payment,
                        sum=sum_,
                        account=account,
                        responsible=request.user,
                    )
                )

        paid_invoices: list[models.PaidInvoice] = []
        unpaid_invoices_numbers = []
        for unpaid_invoice_number, sum_ in data["unpaidInvoices"].items():
            try:
                unpaid_invoice = models.UnpaidInvoice.objects.get(
                    number=unpaid_invoice_number
                )
            except models.UnpaidInvoice.DoesNotExist:
                assert False, f"Неоплаченный счёт {unpaid_invoice_number} не найден"
            unpaid_invoices_numbers.append(unpaid_invoice.number)
            assert unpaid_invoice.can_pay, "Вы не можете платить этот ДО"
            assert (
                0 < sum_ <= unpaid_invoice.allowed_payment_amount
            ), f"{unpaid_invoice_number} сумма должен быть в диапазоне (0, {unpaid_invoice.allowed_payment_amount}]"
            account_data = data["selectedAccounts"]["unpaid-invoices"][0]
            account = models.Account.objects.get(id=account_data["id"])
            project_region = models.ProjectRegion.objects.get(
                id=account_data["projectRegionId"]
            )
            paid_invoices.append(
                models.PaidInvoice(
                    number=unpaid_invoice.number,
                    date=unpaid_invoice.date,
                    invoice_number=unpaid_invoice.invoice_number,
                    invoice_date=unpaid_invoice.invoice_date,
                    project=unpaid_invoice.project,
                    responsible_user_id=unpaid_invoice.responsible_user_id,
                    approver=unpaid_invoice.approver,
                    llc=unpaid_invoice.llc,
                    contractor=unpaid_invoice.contractor,
                    comment=unpaid_invoice.comment,
                    currency=unpaid_invoice.currency,
                    invoice_category=unpaid_invoice.invoice_category,
                    revenue_expense_articles=unpaid_invoice.revenue_expense_articles,
                    sales_order=unpaid_invoice.sales_order,
                    bin_or_iin=unpaid_invoice.bin_or_iin,
                    document_amount=unpaid_invoice.document_amount,
                    iic=unpaid_invoice.iic,
                    payment_destination_code=unpaid_invoice.payment_destination_code,
                    contract_number=unpaid_invoice.contract_number,
                    invoice_amount=unpaid_invoice.invoice_amount,
                    paid_amount_1c=unpaid_invoice.paid_amount_1c,
                    paid=unpaid_invoice.paid,
                    account=account,
                    project_region=project_region,
                    sum=sum_,
                    status=models.default_paid_invoice_status(),
                    responsible=request.user,
                )
            )

        for interdivisional_debt_transfer in data["allInterdivisionalDebtTransfers"]:
            from_whom = models.ProjectRegion.objects.get(
                id=interdivisional_debt_transfer["from-whom"]
            )
            from_account = models.Account.objects.get(
                id=interdivisional_debt_transfer["from-account"]
            )
            to_whom = models.ProjectRegion.objects.get(
                id=interdivisional_debt_transfer["to-whom"]
            )
            to_account = models.Account.objects.get(
                id=interdivisional_debt_transfer["to-account"]
            )
            sum_ = decimal.Decimal(interdivisional_debt_transfer["sum"])
            debts, debt_translate_group = interdivisional_debts_service.translate(
                from_whom=from_whom,
                to_whom=to_whom,
                sum=sum_,
                from_account=from_account,
                to_account=to_account,
                responsible=request.user,
            )
            debt_translate_group.save()
            models.Debt.objects.bulk_create(debts)

        transfers: list[models.Transfer] = []
        for transfer in data["allTransfers"]:
            project_region = models.ProjectRegion.objects.get(
                id=transfer["project-region-id"]
            )
            from_account = models.Account.objects.get(id=transfer["from-account"])
            to_account = models.Account.objects.get(id=transfer["to-account"])
            sum_ = decimal.Decimal(transfer["sum"])
            transfers.append(
                models.Transfer(
                    from_whom=project_region,
                    to_whom=project_region,
                    from_account=from_account,
                    to_account=to_account,
                    sum=sum_,
                    status=models.default_transfer_status(),
                )
            )

        models.MandatoryPaymentSeizure.objects.bulk_create(mandatory_payment_seizures)
        models.PaidInvoice.objects.bulk_create(paid_invoices)

        models.Transfer.objects.bulk_create(transfers)
        models.UnpaidInvoicePMSum.objects.filter(
            number__in=unpaid_invoices_numbers, date=timezone.localdate()
        ).delete()
    except Exception as exception:
        models.Sutochnye.objects.filter(id__in=data["sutochnyeIds"]).delete()
        return JsonResponse({"detail": str(exception)}, status=400)
    return JsonResponse({"detail": "OK"})


def extract_user_id_from_employee_id(employee_id):
    match = re.search(r"(\d+)-", employee_id)
    if match:
        return int(match.group(1))
    return None


@api_view(["GET"])
def get_payment_confirmation(request: Request) -> Response:
    model = request.query_params.get("model")
    id = request.query_params.get("id")
    try:
        payment_confirmation = models.PaymentConfirmationHistory.objects.filter(
            model_name=model, model_id=id
        ).latest("created_at")
    except models.PaymentConfirmationHistory.DoesNotExist:
        return Response({"detail": "Not Found"}, status=404)
    return Response(
        serializers.PaymentConfirmationSerializer(payment_confirmation).data
    )


def get_project_regions(request: HttpRequest) -> JsonResponse:
    director_id = request.GET.get("director-id")
    if not director_id:
        return JsonResponse({"detail": "director_id"}, status=400)
    try:
        director = AvhUser.objects.get(id=director_id)
    except AvhUser.DoesNotExist:
        return JsonResponse({"detail": "director not found"}, status=404)
    project_regions = common_service.get_project_regions(
        director=director, user=request.user
    )
    return JsonResponse(
        {
            "project_regions": serializers.ProjectRegionWithBalanceSerializer(
                project_regions, many=True
            ).data
        }
    )


def get_accounts(request: HttpRequest) -> JsonResponse:
    project_region_id = request.GET.get("project-region-id")
    if not project_region_id:
        return JsonResponse({"detail": "project_region_id"}, status=400)
    try:
        project_region = ProjectRegion.objects.get(id=project_region_id)
    except ProjectRegion.DoesNotExist:
        return JsonResponse({"detail": "project_region not found"}, status=404)
    accounts = common_service.get_project_region_accounts(project_region)
    return JsonResponse(
        {
            "accounts": serializers.AccountWithBalanceSerializer(
                accounts, project_region=project_region, many=True
            ).data
        }
    )


def get_project_region_accounts(request: HttpRequest) -> JsonResponse:
    project_region_id = request.GET.get("project-region-id")
    if not project_region_id:
        return JsonResponse({"detail": "project_region_id"}, status=400)
    try:
        project_region = ProjectRegion.objects.get(id=project_region_id)
    except ProjectRegion.DoesNotExist:
        return JsonResponse({"detail": "project_region not found"}, status=404)
    return JsonResponse(
        {
            "accounts": serializers.AccountSerializer(
                models.Account.objects.filter(available_for=project_region), many=True
            ).data
        }
    )


def get_mandatory_payments_sums(request: HttpRequest) -> JsonResponse:
    date = datetime.date(2023, 1, 1)
    sums = {}
    mandatory_payments = models.MandatoryPayment.objects.all()
    project_regions = common_service.get_project_regions(user=request.user)
    with connection.cursor() as cursor:
        for mandatory_payment in mandatory_payments:
            sums[mandatory_payment.id] = {}
            for project_region in project_regions:
                payment = mandatory_payments_service.get_payment(
                    mandatory_payment=mandatory_payment, project_region=project_region
                )
                sum = payment.sum
                column = {
                    "sum": sum,
                    "project_region": serializers.ProjectRegionSerializer(
                        project_region
                    ).data,
                }
                column["min"] = payment.min
                column["deadline"] = payment.deadline
                column["paid_today"] = payment.paid_today
                column["type"] = payment.type
                sums[mandatory_payment.id][project_region.id] = column
    categories, categories_colspan = mandatory_payments_service.get_categories(
        mandatory_payments
    )
    mandatory_payments_service.annotate_mandatory_payments_with_levels(
        mandatory_payments, categories
    )
    return JsonResponse(
        {
            "categories_colspan": categories_colspan,
            "project_regions": serializers.ProjectRegionSerializer(
                project_regions, many=True
            ).data,
            "mandatory_payments": [
                {
                    "levels": [
                        level
                        and {
                            "category": {
                                "name": level[0].name,
                                "color": level[0].get_color(),
                            },
                            "colspan": level[1],
                            "rowspan": level[2],
                        }
                        for level in mandatory_payment.levels
                    ],
                    "color": mandatory_payment.get_color(),
                    "id": mandatory_payment.id,
                    "name": mandatory_payment.name,
                    "deadline_template": mandatory_payment.deadline_template,
                    "short_deadline_template": mandatory_payment.get_short_deadline_template(),
                }
                for mandatory_payment in mandatory_payments
            ],
            "sums": sums,
        }
    )


def get_interdivisional_debts_data(request: HttpRequest) -> JsonResponse:
    project_region_ids = request.GET.getlist("project-region-id")
    director_ids = request.GET.getlist("director-ids")
    project_regions = common_service.get_project_regions(user=request.user)
    if project_region_ids and director_ids:
        project_regions = project_regions.filter(
            Q(director_id__in=director_ids) | Q(id__in=project_region_ids)
        )
    elif project_region_ids:
        project_regions = project_regions.filter(id__in=project_region_ids)
    elif director_ids:
        project_regions = project_regions.filter(director_id__in=director_ids)
    participants = sorted(interdivisional_debts_service.get_participants())
    project_regions = project_regions.filter(name__in=participants)
    rows = []
    for participant in participants:
        row = []
        for project_region in project_regions:
            if project_region.name == participant:
                sum_ = 0
            else:
                sum_ = interdivisional_debts_service.get_debt_sum(
                    to_whom=participant, from_whom=project_region.name
                )
            row.append({"project_region_id": project_region.id, "sum": round(sum_)})
        if sum(column["sum"] for column in row) == 0:
            continue
        rows.append((participant, row))
    return JsonResponse(
        {
            "participants": participants,
            "directors": serializers.DirectorSerializer(
                AvhUser.objects.filter(
                    id__in=project_regions.values_list("director", flat=True).distinct()
                ),
                many=True,
            ).data,
            "project_regions": serializers.ProjectRegionSerializer(
                project_regions, many=True
            ).data,
            "rows": rows,
        }
    )


@login_required
def runner_and_cash_register(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        services.set_cash_register_sum(decimal.Decimal(request.POST.get("sum")))
    runners = Runner.objects.filter(user=request.user)
    return render(
        request,
        "finance_module/runner_and_cash_register.html",
        {"runners": runners, "cash_register": services.get_cash_register()},
    )


def upload_excel(request):
    User = get_user_model()
    if request.method == "POST":
        uploaded_file = request.FILES.get("file")
        if not uploaded_file:
            messages.error(request, "Ни один файл не загружен.")
            return redirect("finance_module:show_begunok")

        try:
            Runner.objects.all().delete()
            df = pd.read_excel(uploaded_file, skiprows=1)

            # чекает колонки
            required_columns = {"Сумма", "Контрагент", "Статус", "Назначение"}
            if not required_columns.issubset(df.columns):
                messages.error(
                    request, "В файле Excel отсутствуют обязательные столбцы."
                )
                return redirect("finance_module:show_begunok")

            # берет айди пользователя так как там id - FIO
            df["user_id"] = df["Контрагент"].apply(extract_user_id_from_employee_id)

            for index, row in df.iterrows():
                user_id = row["user_id"]
                status = row["Статус"]
                amount = row["Сумма"]
                appointment = row["Назначение"]

                if (
                    pd.notna(user_id)
                    and pd.notna(status)
                    and pd.notna(amount)
                    and pd.notna(appointment)
                    and status == "У кассира, к оплате"
                ):
                    user_email = f"{user_id}@avh.kz"
                    # чекает есть ли в бд юзеры
                    try:
                        user = User.objects.get(email=user_email)
                        Runner.objects.create(
                            user=user,
                            status=status,
                            sum=amount,
                            appointment=appointment,
                        )
                    except User.DoesNotExist:
                        messages.warning(
                            request,
                            f"User with email {user_email} not found in the database.",
                        )

            messages.success(request, "Данные успешно импортированы.")
            return redirect("finance_module:show_begunok")

        except Exception as e:
            messages.error(request, f"Ошибка: {str(e)}")
            return redirect("finance_module:show_begunok")

    return render(request, "finance_module/upload_excel.html")


@smart_table_service.smart_table(
    "unload-paid-invoices", models.PaidInvoice, serializers.PaidInvoiceSerializer
)
def unload_paid_invoices_smart_table(
    request: HttpRequest, queryset: QuerySet, field: str | None = None
) -> QuerySet:
    return queryset.filter(status=models.completed_paid_invoice_status())


@api_view(["GET"])
def get_subdivisions(request: Request) -> Response:
    return Response(
        serializers.SubdivisionSerializer(
            models.Subdivision.objects.all(), many=True
        ).data
    )


@require_POST
@csrf_exempt
def unload(request: HttpRequest) -> HttpResponse:
    data = json.loads(request.body)
    type = data.get("type")
    field_type = data.get("fieldType", {})
    field_values_list = data.get("fieldValuesList", {})
    order = data.get("order", {})
    if not type:
        return JsonResponse(
            {"detail": "Type is requiered in query parameters"}, status=400
        )
    file = None
    if type == "paid-invoices-xlsx-1":
        file = unload_service.unload_paid_invoices_xlsx_1(
            request.user, field_values_list, field_type, order
        )
    elif type == "mandatory-payment-seizures-xlsx-1":
        file = unload_service.unload_mandatory_payment_seizures_xlsx_1(
            request.user, field_values_list, field_type, order
        )
    elif type == "interdivisional-debts-xlsx-1":
        file = unload_service.unload_interdivisional_debts_xlsx_1(
            request.user, field_values_list, field_type, order
        )
    elif type == "unload-paid-invoices-xlsx-2":
        file = unload_logistic_service.unloading_logistic()
    elif type == "unload-1":
        file = unload_service.unload_1()

    if file:
        return FileResponse(file, as_attachment=True)
    return JsonResponse({"detail": f"Unload type {type} does not exists"}, status=404)


def get_project_region_accounts_table(request: HttpRequest) -> JsonResponse:
    if request.GET.get("filter") == "none":
        project_regions = models.ProjectRegion.objects.all()
    else:
        project_regions = common_service.get_project_regions(user=request.user)
        if not project_regions:
            project_regions = models.ProjectRegion.objects.filter(
                id__in=models.ProjectRegionApprover.objects.filter(user=request.user)
                .values_list("project_region", flat=True)
                .distinct()
            )
    if not project_regions:
        return JsonResponse({"detail": "You not have project regions"})
    project_region_accounts = [
        (project_region, common_service.get_project_region_accounts(project_region))
        for project_region in project_regions
    ]
    filter_ = functools.reduce(
        operator.or_,
        (
            (Q(id__in=accounts.values_list("id").distinct()))
            for project_region, accounts in project_region_accounts
        ),
    )
    accounts = models.Account.objects.filter(filter_)
    sums = collections.defaultdict(dict)
    for project_region in project_regions:
        for account in accounts:
            sums[project_region.id][account.id] = common_service.get_account_balance(
                account, project_region
            )

    return JsonResponse(
        {
            "project_region_accounts": {
                project_region.id: serializers.AccountSerializer(
                    accounts, many=True
                ).data
                for project_region, accounts in project_region_accounts
            },
            "project_regions": serializers.ProjectRegionSerializer(
                project_regions, many=True
            ).data,
            "accounts": serializers.AccountSerializer(accounts, many=True).data,
            "sums": sums,
        }
    )


@api_view(["GET"])
def get_table_cell_colors(request: Request) -> Response:
    table_cell_colors = models.TableCellColor.objects.all()
    return Response(
        {
            table_cell_color.key: table_cell_color.color
            for table_cell_color in table_cell_colors
        }
    )


@permission_classes([IsAuthenticated])
@api_view(["POST"])
@transaction.atomic
def setoff(request: Request) -> Response:
    subdivision = request.data.get("subdivision")
    try:
        with transaction.atomic():
            interdivisional_debts_service.setoff(
                request.user, models.Subdivision.objects.get(name=subdivision)
            )
    except models.Subdivision.DoesNotExist:
        return Response(
            {"detail": f"Subdivision with name {subdivision} does not exists"},
            status=404,
        )
    return Response({"detail": "OK"})
