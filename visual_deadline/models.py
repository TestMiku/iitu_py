from django.db import models



# Create your models here.
class ExcelData(models.Model):
    name = models.CharField(max_length=255)
    document_number = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True, default=None)
    end_date = models.CharField(max_length=255, null=True, blank=True, default=None)
    max_deadline = models.DateField(null=True, blank=True, default=None)
    provider = models.CharField(max_length=255,null=True, blank=True, default=None)
    project_manager = models.CharField(max_length=255, null=True, default=None)
    project_group = models.CharField(max_length=255, null=True, blank=True, default=None)
    no_invoice_1C = models.CharField(max_length=255, null=True, blank=True, default=None)
    invoice_date = models.DateField(null=True, blank=True, default=None)
    order_date = models.DateField(null=True, blank=True, default=None)
    project = models.CharField(max_length=255, null=True, default=None)
    deadline = models.CharField(max_length=255, null=True, default=None)
    responsible_sale = models.CharField(max_length=255, null=True, default=None)
    contract_number = models.CharField(max_length=255, null=True, default=None)
    date_document_signed = models.DateField(null=True, blank=True, default=None)
    order_sum = models.CharField(max_length=255, null=True, default=None)
    account_amount = models.CharField(max_length=255, null=True, default=None)
    customer_debt = models.CharField(max_length=255, null=True, default=None)

    # end_date_contract = models.DateField(null=True, blank=True)
    def format_end_date(self) -> str:
        return self.end_date.strftime("%Y-%m.%d")
    def __str__(self):
        return self.name