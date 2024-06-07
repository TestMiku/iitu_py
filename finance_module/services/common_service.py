import collections
import datetime
import decimal
import typing
from functools import cache

import gspread
from django.conf import settings
from django.db import connection
from django.db.models import F, Q, QuerySet, Sum, fields
from django.db.models.functions import Coalesce, TruncDate
from django.utils import timezone

from main.models import AvhUser

from .. import models
from . import mandatory_payments_service


@cache
def get_gspread_client():
    return gspread.service_account(
        settings.BASE_DIR / "finance_module/finane-module-d96b5a587d3c.json"
    )


@cache
def get_document_debt_worksheet():
    return (
        get_gspread_client()
        .open("7_2024_Долги по документам (19.20)")
        .worksheet("Детальная информация")
    )


@cache
def get_technical_list_worksheet():
    return (
        get_gspread_client()
        .open("7_2023_Реестр неоплаченных счетов")
        .worksheet("Техлист")
    )


def get_project_regions(
    *, director: AvhUser | None = None, user: AvhUser | None = None
) -> QuerySet:
    project_regions = mandatory_payments_service.get_ordered_project_regions()
    if director:
        project_regions = project_regions.filter(director=director)
    if user and not user.is_superuser:
        project_regions = project_regions.filter(users=user)
    return project_regions


def get_director_balance(director: AvhUser, user: AvhUser) -> decimal.Decimal:
    project_regions = get_project_regions(director=director, user=user)
    inflows_sum = models.Inflow.objects.filter(
        project_region__in=project_regions
    ).aggregate(sum=Coalesce(Sum("sum"), decimal.Decimal()))["sum"]
    mandatory_payment_seizures_sum = (
        models.MandatoryPaymentSeizure.objects.exclude(
            Q(status__name=models.REJECTED_MANDATORY_PAYMENT_SEIZURE_STATUS_NAME)
            | Q(account__isnull=True)
        )
        .filter(project_region__in=project_regions)
        .aggregate(
            sum=Coalesce(
                Sum("sum"), decimal.Decimal(), output_field=fields.DecimalField()
            )
        )["sum"]
    )
    debt_translate_groups_sum = (
        models.DebtTranslateGroup.objects.exclude(
            Q(to_account__isnull=True)
            | Q(status=models.rejected_debt_translate_group_status())
        )
        .filter(to_whom__in=project_regions.values_list("name", flat=True))
        .aggregate(sum=Coalesce(Sum("sum"), decimal.Decimal()))["sum"]
        - models.DebtTranslateGroup.objects.exclude(
            Q(from_account__isnull=True)
            | Q(status=models.rejected_debt_translate_group_status())
        )
        .filter(from_whom__in=project_regions.values_list("name", flat=True))
        .aggregate(sum=Coalesce(Sum("sum"), decimal.Decimal()))["sum"]
    )
    paid_invoices_sum = (
        models.PaidInvoice.objects.exclude(
            Q(account__isnull=True) | Q(status=models.rejected_paid_invoice_status())
        )
        .filter(project_region__in=project_regions)
        .aggregate(sum=Coalesce(Sum("sum"), decimal.Decimal()))["sum"]
    )
    return (
        inflows_sum
        - mandatory_payment_seizures_sum
        + debt_translate_groups_sum
        - paid_invoices_sum
    )


def get_project_region_balance(project_region: models.ProjectRegion) -> decimal.Decimal:
    inflows_sum = project_region.inflows.aggregate(
        sum=Coalesce(Sum("sum"), decimal.Decimal())
    )["sum"]
    mandatory_payment_seizures_sum = project_region.mandatory_payment_seizures.exclude(
        Q(status__name=models.REJECTED_MANDATORY_PAYMENT_SEIZURE_STATUS_NAME)
        | Q(account__isnull=True)
    ).aggregate(sum=Coalesce(Sum("sum"), decimal.Decimal()))["sum"]
    debt_translate_groups_sum = (
        models.DebtTranslateGroup.objects.exclude(
            Q(to_account__isnull=True)
            | Q(status=models.rejected_debt_translate_group_status())
        )
        .filter(to_whom=project_region)
        .aggregate(sum=Coalesce(Sum("sum"), decimal.Decimal()))["sum"]
        - models.DebtTranslateGroup.objects.exclude(
            Q(from_account__isnull=True)
            | Q(status=models.rejected_debt_translate_group_status())
        )
        .filter(from_whom=project_region)
        .aggregate(sum=Coalesce(Sum("sum"), decimal.Decimal()))["sum"]
    )
    paid_invoices_sum = (
        models.PaidInvoice.objects.exclude(
            Q(account__isnull=True) | Q(status=models.rejected_paid_invoice_status())
        )
        .filter(project_region=project_region)
        .aggregate(sum=Coalesce(Sum("sum"), decimal.Decimal()))["sum"]
    )
    return (
        inflows_sum
        - mandatory_payment_seizures_sum
        + debt_translate_groups_sum
        - paid_invoices_sum
    )


def get_administrative_account() -> models.Account:
    return models.Account.objects.get_or_create(
        name="АДМ", number="KZ208562203106786042"
    )[0]


def get_account_balance(
    account: models.Account,
    project_region: models.ProjectRegion | None = None,
    irrelevant: bool = False,
) -> decimal.Decimal:
    administrative_account = get_administrative_account()
    if account == administrative_account:
        mandatory_payment_seizures_sum = (
            models.MandatoryPaymentSeizure.objects.exclude(
                Q(imported_from_file=True) | Q(account__isnull=True)
            )
            .filter(status=models.completed_mandatory_payment_seizure_status())
            .aggregate(sum=Coalesce(Sum("sum"), decimal.Decimal()))["sum"]
        )
        return mandatory_payment_seizures_sum
    inflows = account.inflows
    if project_region:
        inflows = inflows.filter(project_region=project_region)
    if irrelevant:
        inflows = inflows.exclude(date=timezone.localdate())
    inflows_sum = inflows.aggregate(
        remainder_total_sum=Coalesce(Sum("remainder"), decimal.Decimal())
    )["remainder_total_sum"]
    mandatory_payment_seizures = account.mandatory_payment_seizures.exclude(
        Q(status__name=models.REJECTED_MANDATORY_PAYMENT_SEIZURE_STATUS_NAME)
        | Q(account__isnull=True)
    )
    if project_region:
        mandatory_payment_seizures = mandatory_payment_seizures.filter(
            project_region=project_region
        )
    if irrelevant:
        mandatory_payment_seizures = mandatory_payment_seizures.annotate(
            datetime_date=TruncDate("datetime")
        ).exclude(datetime_date=timezone.localdate())
    mandatory_payment_seizures_sum = mandatory_payment_seizures.aggregate(
        sum=Coalesce(Sum("sum"), decimal.Decimal())
    )["sum"]

    debt_translate_groups1 = models.DebtTranslateGroup.objects.exclude(
        status=models.rejected_debt_translate_group_status()
    ).filter(to_account=account)
    if project_region:
        debt_translate_groups1 = debt_translate_groups1.filter(
            to_whom=project_region.name
        )
    if irrelevant:
        debt_translate_groups1 = debt_translate_groups1.annotate(
            datetime_date=TruncDate("datetime")
        ).exclude(datetime_date=timezone.localdate())
    debt_translate_groups2 = models.DebtTranslateGroup.objects.exclude(
        status=models.rejected_debt_translate_group_status()
    ).filter(from_account=account)
    if project_region:
        debt_translate_groups2 = debt_translate_groups2.filter(
            from_whom=project_region.name
        )
    if irrelevant:
        debt_translate_groups2 = debt_translate_groups2.annotate(
            datetime_date=TruncDate("datetime")
        ).exclude(datetime_date=timezone.localdate())
    debt_translate_groups_sum = (
        debt_translate_groups1.aggregate(sum=Coalesce(Sum("sum"), decimal.Decimal()))[
            "sum"
        ]
        - debt_translate_groups2.aggregate(sum=Coalesce(Sum("sum"), decimal.Decimal()))[
            "sum"
        ]
    )
    transfers1 = models.Transfer.objects.filter(to_account=account)
    if project_region:
        transfers1 = transfers1.filter(to_whom=project_region)
    if irrelevant:
        transfers1 = transfers1.annotate(datetime_date=TruncDate("datetime")).exclude(
            datetime_date=timezone.localdate()
        )
    transfers2 = models.Transfer.objects.filter(from_account=account)
    if project_region:
        transfers2 = transfers2.filter(from_whom=project_region)
    if irrelevant:
        transfers2 = transfers2.annotate(datetime_date=TruncDate("datetime")).exclude(
            datetime_date=timezone.localdate()
        )
    transfers_sum = (
        transfers1.aggregate(sum=Coalesce(Sum("sum"), decimal.Decimal()))["sum"]
        - transfers2.aggregate(sum=Coalesce(Sum("sum"), decimal.Decimal()))["sum"]
    )
    paid_invoices = models.PaidInvoice.objects.exclude(
        status=models.rejected_paid_invoice_status()
    ).filter(account=account)
    if project_region:
        paid_invoices = paid_invoices.filter(project_region=project_region)
    if irrelevant:
        paid_invoices = paid_invoices.annotate(at_date=TruncDate("at")).exclude(
            at_date=timezone.localdate()
        )
    paid_invoices_sum = paid_invoices.annotate(
        sum_with_commission=F("sum") + F("commission")
    ).aggregate(sum=Coalesce(Sum("sum_with_commission"), decimal.Decimal()))["sum"]

    sutochnye = models.Sutochnye.objects.exclude(
        status=models.rejected_sutochnye_status()
    ).filter(account=account)
    if project_region:
        sutochnye = sutochnye.filter(project_region=project_region)
    if irrelevant:
        sutochnye = sutochnye.annotate(created_at_date=TruncDate("created_at")).exclude(
            created_at_date=timezone.localdate()
        )
    sutochnye_sum = sutochnye.aggregate(sum=Coalesce(Sum("sum"), decimal.Decimal()))[
        "sum"
    ]
    administrative_transfers = models.AdministrativeTransfer.objects.exclude(
        status=models.rejected_administrative_transfer_status()
    ).filter(account=account)
    if project_region:
        administrative_transfers = administrative_transfers.filter(
            project_region=project_region
        )
    administrative_transfers_sum = administrative_transfers.aggregate(
        sum=Coalesce(Sum("sum"), decimal.Decimal())
    )["sum"]

    raschetnye = models.Raschetnye.objects.exclude(status=models.rejected_raschetnye_status()).filter(account=account)
    if project_region:
        raschetnye = raschetnye.filter(project_region=project_region)
    raschetnye_sum = raschetnye.aggregate(sum=Coalesce(Sum(F("raschetnye_by_1c") + F("subreport")), decimal.Decimal()))["sum"]

    chsi = models.CHSI.objects.exclude(group__status=models.rejected_chsi_group_status()).filter(group__account=account)
    if project_region:
        chsi = chsi.filter(group__project_region=project_region)
    chsi_groups_sum = chsi.aggregate(sum=Coalesce(Sum("sum"), decimal.Decimal()))["sum"]

    return (
        inflows_sum
        - mandatory_payment_seizures_sum
        - paid_invoices_sum
        - sutochnye_sum
        - administrative_transfers_sum
        - raschetnye_sum
        - chsi_groups_sum
        + debt_translate_groups_sum
        + transfers_sum
    )


def get_project_region_accounts(project_region: models.ProjectRegion) -> QuerySet:
    return project_region.accounts.all()


def mandatory_payments_paid(user: AvhUser) -> bool:
    if user.is_superuser:
        return True
    today = timezone.localdate()
    if models.AccessToOthersExceptionForProjectManager.objects.filter(
        project_manager=user,
        datetime__year=today.year,
        datetime__month=today.month,
        datetime__day=today.day,
    ).exists():
        return True
    for project_region in get_project_regions(user=user):
        for mandatory_payment in models.MandatoryPayment.objects.all():
            payment = mandatory_payments_service.get_payment(project_region=project_region, mandatory_payment=mandatory_payment)
            if payment.type in ("soon", "overdue") and not payment.paid_today:
                return False
    return True


def get_project_region_mandatory_payments_paid(user: AvhUser) -> dict[int, bool]:
    project_region_mandatory_payments_paid = {}
    today = timezone.localdate()
    exception = models.AccessToOthersExceptionForProjectManager.objects.filter(
        project_manager=user,
        datetime__year=today.year,
        datetime__month=today.month,
        datetime__day=today.day,
    ).exists()
    for project_region in get_project_regions(user=user):
        project_region_mandatory_payments_paid[project_region.id] = True
        if user.is_superuser or exception:
            continue
        for mandatory_payment in models.MandatoryPayment.objects.all():
            payment = mandatory_payments_service.get_payment(project_region=project_region, mandatory_payment=mandatory_payment)
            if payment.type in ("soon", "overdue"):
                project_region_mandatory_payments_paid[project_region.id] = project_region_mandatory_payments_paid[project_region.id] and payment.paid_today
    return project_region_mandatory_payments_paid
