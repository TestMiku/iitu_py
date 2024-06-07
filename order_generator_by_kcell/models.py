from django.db import models

# Create your models here.

class TCPModel(models.Model):
    document_number = models.CharField(max_length=50)
    unit_price = models.FloatField()