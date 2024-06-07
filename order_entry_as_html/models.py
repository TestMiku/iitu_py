from django.db import models


class OrderRegion(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=256)

    def __str__(self) -> str:
        return self.name


class TCP0(models.Model):
    customer = models.CharField(max_length=256)
    customer_tcp = models.CharField(max_length=512)
    contractor_tcp = models.CharField(max_length=512)
    price = models.DecimalField(max_digits=19, decimal_places=2)
    measuring_unit = models.CharField(max_length=256)
    find_key = models.CharField(max_length=256, unique=True)
