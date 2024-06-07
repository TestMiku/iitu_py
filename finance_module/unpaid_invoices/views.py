import datetime
import decimal
import json
import mimetypes
import typing

import django.core.mail
from django.db.models import QuerySet
from django.db.models.functions import TruncDate
from django.http import FileResponse, HttpRequest, HttpResponse, JsonResponse
from django.utils import timezone
from django.views import generic
from django.views.decorators.http import require_GET, require_POST
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from finance_module import serializers
from finance_module.services.smart_table_service import smart_table
from finance_module.services.unload_service import unload_1c

from .. import models
from ..services import unload_logistic_service, unpaid_invoices_service


class PaidInvoices(generic.TemplateView):
    template_name = "finance_module/unpaid_invoices/paid_invoices.html"


class ListTemplateView(generic.TemplateView):
    template_name = "finance_module/unpaid_invoices/list.html"

    def get_context_data(self, **kwargs):
        return super().get_context_data(
            unpaid_invoices=models.UnpaidInvoice.objects.all(), **kwargs
        )


class ImportTemplateView(generic.TemplateView):
    template_name = "finance_module/unpaid_invoices/import.html"

    def post(self, request: HttpRequest) -> HttpResponse:
        post_type = request.POST.get("post-type")
        if post_type == "import-19-33-1":
            file = request.FILES.get("file")
            if file:
                file = file.file
            unpaid_invoices_service.import_unpaid_invoices(bytes_io=file)
        elif post_type == "import-work-statuses":
            unpaid_invoices_service.import_unpaid_invoices_work_statuses()
        elif post_type == "import-payment-destination-codes":
            unpaid_invoices_service.import_unpaid_invoices_payment_destination_codes()
        return self.get(request)


class UnloadingInvoicesPaidListView(generic.ListView):
    template_name = "finance_module/unpaid_invoices/unloading_paid.html"

    def get_queryset(self):
        return models.UnpaidInvoice.objects.all()

    def get(self, request, *args, **kwargs):
        unpaid_invoice = request.GET.get("unpaid_invoice")
        logistic = request.GET.get("logistic")

        if unpaid_invoice == "":
            file = unpaid_invoices_service.upload_paid_invoices()
            return FileResponse(file, filename="unloading_paid.xlsx")
        elif logistic == "":
            file = unload_logistic_service.unloading_logistic()
            return FileResponse(file, filename="unloading_logistic.xlsx")

        return super().get(request, *args, **kwargs)


class PMSumTemplateView(generic.TemplateView):
    template_name = "finance_module/unpaid_invoices/pm_sum.html"

    def get_context_data(self, **kwargs: typing.Any) -> dict[str, typing.Any]:
        return super().get_context_data(**kwargs)


@require_POST
def update_pm_sum(request: HttpRequest) -> JsonResponse:
    data = json.loads(request.body)
    number = data["number"]
    sum_ = decimal.Decimal(data["sum"])
    try:
        unpaid_invoice = models.UnpaidInvoice.objects.get(number=number)
    except models.UnpaidInvoice.DoesNotExist:
        pass
    else:
        if unpaid_invoice.payment_decision != "OK":
            return JsonResponse({"detail": 'Решение по оплате не "ОК"'})
        if sum_ < 0 or sum_ > unpaid_invoice.allowed_payment_amount:
            return JsonResponse(
                {
                    "detail": f"Сумма должна быть в диапазоне [0, {unpaid_invoice.allowed_payment_amount}]"
                }
            )
    models.UnpaidInvoicePMSum.objects.update_or_create(
        number=number, date=timezone.localdate(), defaults={"sum": sum_}
    )
    return JsonResponse({"detail": "OK"})


@require_GET
def get_pm_sum(request: HttpRequest) -> JsonResponse:
    number = request.GET.get("number")
    try:
        pm_sum = models.UnpaidInvoicePMSum.objects.get(
            number=number, date=timezone.localdate()
        )
    except models.UnpaidInvoicePMSum:
        return JsonResponse({"sum": None})
    return JsonResponse({"sum": pm_sum.sum})


@smart_table("paid-invoices", models.PaidInvoice, serializers.PaidInvoiceSerializer)
def paid_invoices_smart_table(
    request: HttpRequest, queryset: QuerySet, field: str | None = None
) -> QuerySet:
    return queryset.filter(status=models.completed_paid_invoice_status())


@smart_table(
    "unpaid-invoices", models.UnpaidInvoice, serializers.UnpaidInvoiceSerializer
)
def unpaid_invoices_smart_table(
    request: HttpRequest, queryset: QuerySet, field: str | None = None
):
    return unpaid_invoices_service.annotate_unpaid_invoices(queryset)


@api_view(["POST"])
def mail_1c(request: Request) -> Response:
    MAIL = "22293@avh.kz"
    queryset = models.PaidInvoice.objects.annotate(at_date=TruncDate("at")).filter(
        status=models.completed_paid_invoice_status(), at_date=timezone.localdate()
    )
    file_1c = unload_1c(queryset)
    email_message = django.core.mail.EmailMessage(
        subject="1C", body="ПП готово", to=[MAIL]
    )
    email_message.attach("1C.xlsx", file_1c.read(), mimetypes.types_map[".xlsx"])
    email_message.send()
    return Response({"detail": f"Отправлен на почту {MAIL}"})
