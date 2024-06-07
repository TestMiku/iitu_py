import datetime
from django.test import TestCase

from . import models
from .services.mandatory_payments_service import get_payment


class AnimalTestCase(TestCase):
    def setUp(self) -> None:
        mandatory_payment = models.MandatoryPayment.objects.create(name="Алматы Картел")
        project_region = models.ProjectRegion.objects.create(name="ЗП 01")
        models.MandatoryPaymentAccrual.objects.bulk_create(
            [
                models.MandatoryPaymentAccrual(
                    mandatory_payment=mandatory_payment,
                    project_region=project_region,
                    sum=100000,
                    datetime=datetime.datetime(2024, 10, 10),
                    deadline=datetime.date(2024, 10, 15)
                )
            ]
        )
        models.MandatoryPaymentSeizure.objects.bulk_create(
            [
                models.MandatoryPaymentSeizure(
                    mandatory_payment=mandatory_payment,
                    project_region=project_region,
                    sum=50000,
                    datetime=datetime.datetime(2024, 10, 10)
                )
            ]
        )

    def test_payment(self):
        mandatory_payment = models.MandatoryPayment.objects.get(name="Алматы Картел")
        project_region = models.ProjectRegion.objects.get(name="ЗП 01")
        payment = get_payment(mandatory_payment=mandatory_payment, project_region=project_region)
