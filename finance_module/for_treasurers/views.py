import mimetypes
import pathlib
from typing import Any

import django.core.mail
from django.db.models import Case, F, Model, Q, QuerySet, Value, When
from django.db.models.fields import CharField
from django.db.models.functions import Concat
from django.http import Http404, HttpRequest, HttpResponse
from django.views import generic
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from finance_module.services.smart_table_service import smart_table

from .. import models, serializers


class ConfirmationTemplateView(generic.TemplateView):
    template_name = "finance_module/for_treasurers/confirmation.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return super().get_context_data(
            mandatory_payment_seizures=models.MandatoryPaymentSeizure.objects.filter(
                status=models.sent_for_second_confirmation_mandatory_payment_seizure_status()
            ),
            paid_invoices=models.PaidInvoice.objects.filter(
                status=models.default_paid_invoice_status()
            ),
            debt_translate_groups=models.DebtTranslateGroup.objects.filter(
                status=models.default_debt_translate_group_status()
            ),
            transfers=models.Transfer.objects.filter(
                status=models.default_transfer_status()
            ),
            sutochnyes=models.Sutochnye.objects.filter(
                status=models.default_sutochnye_status()
            ),
            **kwargs,
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        post_type = request.POST.get("post-type")
        responsible = self.request.user if self.request.user.is_authenticated else None
        if post_type == "confirmation-mandatory-payment-seizures":
            for mandatory_payment_seizure_id in request.POST.getlist(
                "mandatory-payment-seizure-id"
            ):
                mandatory_payment_seizure = models.MandatoryPaymentSeizure.objects.get(
                    id=mandatory_payment_seizure_id
                )
                confirm = request.POST.get(f"confirm-{mandatory_payment_seizure_id}")
                if confirm == "complete":
                    mandatory_payment_seizure.complete(responsible=responsible)
                else:
                    reject_comment = request.POST.get(
                        f"reject-comment-{mandatory_payment_seizure_id}"
                    ) or request.POST.get("common-reject-comment")
                    mandatory_payment_seizure.reject(
                        responsible=responsible, reject_comment=reject_comment
                    )
        elif post_type == "confirmation-paid-invoices":
            for paid_invoice_id in request.POST.getlist("paid-invoice-id"):
                paid_invoice = models.PaidInvoice.objects.get(id=paid_invoice_id)
                confirm = request.POST.get(f"confirm-{paid_invoice_id}")

                if confirm == "complete":
                    paid_invoice.complete(responsible=responsible)
                else:
                    reject_comment = request.POST.get(
                        f"reject-comment-{paid_invoice_id}"
                    ) or request.POST.get("common-reject-comment")
                    paid_invoice.reject(
                        responsible=responsible, reject_comment=reject_comment
                    )
        elif post_type == "confirmation-debt-translate-groups":
            for debt_translate_group_id in request.POST.getlist(
                "debt-translate-group-id"
            ):
                debt_translate_group = models.DebtTranslateGroup.objects.get(
                    id=debt_translate_group_id
                )
                confirm = request.POST.get(f"confirm-{debt_translate_group_id}")

                if confirm == "complete":
                    debt_translate_group.complete(responsible=responsible)
                else:
                    reject_comment = request.POST.get(
                        f"reject-comment-{debt_translate_group_id}"
                    ) or request.POST.get("common-reject-comment")
                    debt_translate_group.reject(
                        responsible=responsible, reject_comment=reject_comment
                    )
        elif post_type == "confirmation-transfers":
            for transfer_id in request.POST.getlist("transfer-id"):
                transfer = models.Transfer.objects.get(id=transfer_id)
                confirm = request.POST.get(f"confirm-{transfer_id}")
                if confirm == "complete":
                    transfer.complete(responsible=responsible)
                else:
                    reject_comment = request.POST.get(
                        f"reject-comment-{transfer_id}"
                    ) or request.POST.get("common-reject-comment")
                    transfer.reject(
                        responsible=responsible, reject_comment=reject_comment
                    )

        elif post_type == "confirmation-sutochnye":
            for sutochnye_id in request.POST.getlist("sutochnye-id"):
                sutochnye = models.Sutochnye.objects.get(id=sutochnye_id)
                confirm = request.POST.get(f"confirm-{sutochnye_id}")
                if confirm == "complete":
                    sutochnye.complete(responsible=responsible)
                else:
                    reject_comment = request.POST.get(
                        f"reject-comment-{sutochnye_id}"
                    ) or request.POST.get("common-reject-comment")
                    sutochnye.reject(
                        responsible=responsible, reject_comment=reject_comment
                    )
        else:
            raise Http404
        return self.get(request)


@smart_table(
    "mandatory-payment-seizures",
    models.MandatoryPaymentSeizure,
    serializers.MandatoryPaymentSeizureSerializer,
)
def mandatory_payment_seizures_smart_table(
    request: HttpRequest, queryset: QuerySet, field: str | None = None
) -> QuerySet:
    return queryset.exclude(imported_from_file=True).annotate(
        responsible_name=Case(
            When(
                Q(responsible__isnull=False),
                then=Concat(
                    "responsible__first_name", Value(" "), "responsible__last_name"
                ),
            )
        ),
        can_be_confirmed=Q(
            status=models.sent_for_second_confirmation_mandatory_payment_seizure_status()
        ),
    )


@smart_table(
    "paid-invoices",
    models.PaidInvoice,
    serializers.PaidInvoiceSerializer,
)
def paid_invoices_smart_table(
    request: HttpRequest, queryset: QuerySet, field: str | None = None
) -> QuerySet:
    return queryset.annotate(
        responsible_name=Case(
            When(
                Q(responsible__isnull=False),
                then=Concat(
                    "responsible__first_name", Value(" "), "responsible__last_name"
                ),
            )
        ),
        can_be_confirmed=Q(status=models.default_paid_invoice_status()),
    )


@smart_table(
    "debt-translate-groups",
    models.DebtTranslateGroup,
    serializers.DebtTranslateGroupSerializer,
)
def debt_translate_groups_smart_table(
    request: HttpRequest, queryset: QuerySet, field: str | None = None
) -> QuerySet:
    return queryset.annotate(
        same_accounts=Q(from_account=F("to_account")),
        responsible_name=Case(
            When(
                Q(responsible__isnull=False),
                then=Concat(
                    "responsible__first_name", Value(" "), "responsible__last_name"
                ),
            )
        ),
        can_be_confirmed=Q(status=models.default_debt_translate_group_status()),
    ).exclude(same_accounts=True)


@smart_table(
    "transfers",
    models.Transfer,
    serializers.TransferSerializer,
)
def transfers_smart_table(
    request: HttpRequest, queryset: QuerySet, field: str | None = None
) -> QuerySet:
    return queryset.annotate(
        responsible_name=Case(
            When(
                Q(responsible__isnull=False),
                then=Concat(
                    "responsible__first_name", Value(" "), "responsible__last_name"
                ),
            )
        ),
        can_be_confirmed=Q(status=models.default_transfer_status()),
    )


@smart_table(
    "sutochnye",
    models.Sutochnye,
    serializers.SutochnyeSerializer,
)
def sutochnye_smart_table(
    request: HttpRequest, queryset: QuerySet, field: str | None = None
) -> QuerySet:
    return queryset.annotate(
        # responsible_name=Case(
        #     When(
        #         Q(responsible__isnull=False),
        #         then=Concat(
        #             "responsible__first_name", Value(" "), "responsible__last_name"
        #         ),
        #     )
        # ),
        business_trip_period=Concat(
            "business_trip_start_date",
            Value(" - "),
            "business_trip_end_date",
            output_field=CharField(),
        ),
        can_be_confirmed=Q(status=models.default_sutochnye_status()),
    )


@smart_table(
    "administrative-transfers",
    models.AdministrativeTransfer,
    serializers.AdministrativeTransferSerializer,
)
def administrative_transfers_smart_table(
    request: HttpRequest, queryset: QuerySet, field: str | None = None
) -> QuerySet:
    return queryset.annotate(
        can_be_confirmed=Q(status=models.default_administrative_transfer_status())
    )


@smart_table(
    "confirmation-history",
    models.PaymentConfirmationHistory,
    serializers.PaymentConfirmationSerializer,
)
def payment_confirmation_history_smart_table(
    request: HttpRequest, queryset: QuerySet, field: str | None = None
) -> QuerySet:
    return queryset.annotate(
        responsible_name=Case(
            When(
                Q(responsible__isnull=False),
                then=Concat(
                    "responsible__first_name", Value(" "), "responsible__last_name"
                ),
            )
        ),
    )


@permission_classes([IsAuthenticated])
@api_view(["POST"])
def confirmation(request: Request) -> Response:
    model: type[Model] = getattr(models, request.data.get("model"), None)
    if not model:
        return Response({}, status=404)

    for id in request.data.getlist("id"):
        instance = model.objects.get(id=id)
        confirmation = request.data.get(f"confirmation-{id}")
        if confirmation == "reject":
            reject_comment = request.data.get(f"reject-comment-{id}")
            instance.reject(responsible=request.user, reject_comment=reject_comment)
        else:
            instance.complete(responsible=request.user)
    return Response({"detail": "OK"})


@permission_classes([IsAuthenticated])
@api_view(["POST"])
def mail_accountant(request: Request, pk: int) -> Response:
    MAIL = "22293@avh.kz"
    sutochnye = models.Sutochnye.objects.get(pk=pk)
    email_message = django.core.mail.EmailMessage(
        subject="Суточное",
        body="Просьба предоставить SWIFT",
        to=[MAIL],
    )
    for file in sutochnye.files.all():
        email_message.attach(
            pathlib.Path(file.file.name).name,
            file.file.read(),
            mimetypes.types_map[".xlsx"],
        )
    email_message.send()
    return Response({"detail": f"Отправлен на почту {MAIL}"})


@permission_classes([IsAuthenticated])
@api_view(["POST"])
def mail_000(request: Request, pk: int) -> Response:
    MAIL = "22293@avh.kz"
    sutochnye = models.Sutochnye.objects.get(pk=pk)
    email_message = django.core.mail.EmailMessage(
        subject="Суточное",
        body="ПП готово",
        to=[MAIL],
    )
    for file in sutochnye.files.all():
        email_message.attach(
            pathlib.Path(file.file.name).name,
            file.file.read(),
            mimetypes.types_map[".xlsx"],
        )
    email_message.send()
    return Response({"detail": f"Отправлен на почту {MAIL}"})
