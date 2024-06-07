from django.db import models


class Handbook(models.Model):
    code = models.CharField(max_length=20, null=True, blank=True)
    quantity = models.CharField(max_length=300, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    unit = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.name or ""
    
    class Meta:
        db_table = 'handbook_model'
