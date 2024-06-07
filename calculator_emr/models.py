from django.db import models


class dataTCP(models.Model):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=50, null=True)
    max_sum = models.FloatField(null=True)
    search_key = models.CharField(max_length=100, null=True)
    

class dataBS(models.Model):
    order_number = models.CharField(max_length=255)
    order_sem_with_nds = models.FloatField(default=0)
    order_sem_without_nds = models.FloatField(default=0)
    kind_of_activity = models.CharField(max_length=255, null=True)
    field_of_activity = models.CharField(max_length=50, null=True)
    region = models.CharField(max_length=255, null=True)
    project = models.CharField(max_length=255, null=True)
    customer = models.CharField(max_length=255)
    order_entry_date = models.DateField(max_length=50, null=True)


class data1922(models.Model):
    order_number = models.CharField(max_length=255, null=True)
    doc_number = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    name = models.CharField(max_length=255, null=True)
    supplier = models.CharField(max_length=255)
    comment = models.TextField(null=True, blank=True)
    payamt1c = models.FloatField(default=0, null=True)
    notpayamt1c = models.FloatField(default=0, null=True)
    totallines = models.FloatField(default=0, null=True)
    paid1c = models.FloatField(default=0, null=True)
    notpaid1c = models.FloatField(default=0, null=True)
    projects_group = models.CharField(max_length=255, null=True)
