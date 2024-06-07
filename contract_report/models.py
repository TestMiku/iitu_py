from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta


class Supplier(models.Model):
    name = models.CharField(max_length=80, null=True, blank=True)
    bin = models.CharField(max_length=20, null=True, blank=True)
    limit_days = models.IntegerField(null=True, blank=True)
    sum_of_limit = models.IntegerField(null=True, blank=True)
    too = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.bin} - {self.limit_days} - {self.sum_of_limit} - {self.too}'


class Adem_19_20(models.Model):
    documentno = models.IntegerField(null=True, blank=True)
    nscheta = models.CharField(max_length=80, null=True, blank=True)
    datascheta = models.DateField(null=True, blank=True)
    gruppa_proekrov = models.CharField(max_length=80, null=True, blank=True)
    too = models.CharField(max_length=80, null=True, blank=True)
    postavshik = models.CharField(max_length=80, null=True, blank=True)
    notpayamt1ckzt = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    bin = models.CharField(max_length=20, null=True, blank=True)
    docserviceact = models.CharField(max_length=80, null=True, blank=True)
    docdate = models.DateField(null=True, blank=True)
    quantity = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.documentno} - {self.bin} - {self.postavshik}'


class ESF_A77(models.Model):
    too = models.CharField(max_length=80, null=True, blank=True)
    postavshik = models.CharField(max_length=80, null=True, blank=True)
    bin = models.CharField(max_length=20, null=True, blank=True)
    quantity = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    dateinvoiced = models.DateField(null=True, blank=True)

    def __str__(self):
        try:
            bin_str = str(int(float(self.bin))
                          ) if self.bin is not None else str(self.bin)
        except (ValueError, TypeError):
            bin_str = str(self.bin)
        return f'{self.postavshik} - {bin_str}'

    def get_bin_as_int(self):
        return int(self.bin) if self.bin else None


class Merged_model(models.Model):
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    documentno = models.IntegerField(null=True, blank=True)
    nscheta = models.CharField(max_length=80, null=True, blank=True)
    datascheta = models.DateField(null=True, blank=True)
    too = models.CharField(max_length=80, null=True, blank=True)
    postavshik = models.CharField(max_length=80, null=True, blank=True)
    bin = models.CharField(max_length=20, null=True, blank=True)
    notpayamt1ckzt = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, blank=True)
    gruppa_proekrov = models.CharField(max_length=80, null=True, blank=True)
    docdate = models.DateField(null=True, blank=True)
    matched = models.BooleanField(default=False)

    def get_current_date(self):
        return datetime.now().strftime('%d.%m.%Y')

    def get_supplier_limit_days(self):
        supplier = Supplier.objects.filter(
            bin=self.bin, name=self.postavshik,too=self.too).first()
        if supplier:
            return supplier.limit_days
        return None

    def get_supplier_sum_of_limit(self):
        supplier = Supplier.objects.filter(
            bin=self.bin, name=self.postavshik,too=self.too).first()
        if supplier:
            return supplier.sum_of_limit
        return None

    def how_many_days_have_passed(self):
        if self.docdate:
            try:
                current_date = datetime.now().date()
                difference = (current_date - self.docdate).days
                return difference
            except Exception as e:
                return None
        else:
            try:
                current_date = datetime.now().date()
                difference = (current_date - self.datascheta).days
                return difference
            except Exception as e:
                return None

    def days_before_payment(self):
        supplier_limit_days = self.get_supplier_limit_days()
        days_passed = self.how_many_days_have_passed()
        if supplier_limit_days is not None and days_passed is not None:
            return supplier_limit_days - days_passed
        else:
            return None 

    def date_of_payment(self):
        if self.docdate:
            try:
                payment_date = self.docdate + timedelta(days=self.get_supplier_limit_days())
                return payment_date
            except Exception as e:
                return None
        else:
            try:
                payment_date = self.datascheta + timedelta(days=self.get_supplier_limit_days())
                return payment_date
            except Exception as e:
                return None
        return None

    # def __str__(self):
    #     return self.documentno
