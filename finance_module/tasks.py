from celery import shared_task
from django.utils import timezone

from .services.unpaid_invoices_service import (
    import_unpaid_invoices,
    import_unpaid_invoices_payment_destination_codes,
    import_unpaid_invoices_work_statuses,
)


@shared_task
def import_unpaid_invoices_shared_task() -> None:
    now = timezone.localtime()
    if now.hour in [11, 15] and now.minute == 45:
        import_unpaid_invoices()
        import_unpaid_invoices_work_statuses()
        import_unpaid_invoices_payment_destination_codes()
