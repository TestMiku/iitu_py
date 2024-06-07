from django.db import models

# Create your models here.

class GoogleSheetData(models.Model):
    nomenclature = models.CharField(max_length=512)
    account_number = models.CharField(max_length=512)
    account_number_splited = models.CharField(max_length=512)
    quantity = models.CharField(max_length=512, null=True)
    unit_measurement = models.CharField(max_length=512)
    price = models.CharField(max_length=512)
    nomenclature_code = models.CharField(max_length=512, null=True)
    order_number = models.CharField(max_length=512)
    tax = models.CharField(max_length=512, null=True)
    table_type = models.CharField(max_length=10, default='main')