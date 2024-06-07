from django.db import models
from django.contrib.auth.models import User, Permission
from django.db.models.signals import pre_save
from django.dispatch import receiver
from pandas import NaT
import datetime
import calendar

# Create your models here.
class MainModel(models.Model):
    
    def __str__(self) -> str:
        return self.order_number or "None"
    
    order_number = models.CharField(max_length=255, null=True, blank=True)
    order_entered_date = models.CharField(max_length=255, null=True, blank=True)
    order_entered_date_month = models.CharField(max_length=255, null=True, blank=True)
    order_entered_date_year = models.CharField(max_length=255, null=True, blank=True)
    podryad_transfer = models.CharField(max_length=255, null=True, blank=True)
    podryad_transfer_month = models.CharField(max_length=255, null=True, blank=True)
    podryad_transfer_year = models.CharField(max_length=255, null=True, blank=True)
    order_number_for_work = models.CharField(max_length=255, null=True, blank=True)
    signed_order_date = models.CharField(max_length=255, null=True, blank=True)
    signed_order_date_month = models.CharField(max_length=255, null=True, blank=True)
    signed_order_date_year = models.CharField(max_length=255, null=True, blank=True)
    work_period_days = models.CharField(max_length=255, null=True, blank=True)
    finish_date_plan = models.CharField(max_length=255, null=True, blank=True)
    left_days_to_finish = models.CharField(max_length=255, null=True, blank=True)
    agreement_status = models.CharField(max_length=255, null=True, blank=True)
    customer = models.CharField(max_length=255, null=True, blank=True)
    provider = models.CharField(max_length=255, null=True, blank=True)
    pm = models.CharField(max_length=255, null=True, blank=True)
    project = models.CharField(max_length=255, null=True, blank=True)
    agreement_attachment = models.CharField(max_length=255, null=True, blank=True)
    partition = models.CharField(max_length=255, null=True, blank=True)
    project_group = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    activity_field = models.CharField(max_length=255, null=True, blank=True)
    activity_type = models.CharField(max_length=255, null=True, blank=True)
    service_range = models.CharField(max_length=255, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    contract_number = models.CharField(max_length=255, null=True, blank=True)
    contract_sign_date = models.CharField(max_length=255, null=True, blank=True)
    order_sum_vat = models.CharField(max_length=255, null=True, blank=True)
    plan_month = models.CharField(max_length=255, null=True, blank=True)
    plan_year = models.CharField(max_length=255, null=True, blank=True)
    plan_month_new = models.CharField(max_length=255, null=True, blank=True)
    plan_year_new = models.CharField(max_length=255, null=True, blank=True)
    error = models.CharField(max_length=255, null=True, blank=True)
    comment_finance = models.CharField(max_length=255, null=True, blank=True)
    comment_pm = models.CharField(max_length=255, null=True, blank=True)
    account_number_avans = models.CharField(max_length=255, null=True, blank=True)
    date_invoice = models.CharField(max_length=255, null=True, blank=True)
    date_avans = models.CharField(max_length=255, null=True, blank=True)
    date_avans_year = models.CharField(max_length=255, null=True, blank=True)
    avans_sum = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=255, null=True, blank=True)
    invoice_faktura_number = models.CharField(max_length=255, null=True, blank=True)
    date_invoice_release = models.CharField(max_length=255, null=True, blank=True)
    date_invoice_release_month = models.CharField(max_length=255, null=True, blank=True)
    date_invoice_release_year = models.CharField(max_length=255, null=True, blank=True)
    sum_by_invoice = models.CharField(max_length=255, null=True, blank=True)
    work_type = models.CharField(max_length=255, null=True, blank=True)
    on_who = models.CharField(max_length=255, null=True, blank=True)
    work_status = models.CharField(max_length=255, null=True, blank=True)
    work_finish_month = models.CharField(max_length=255, null=True, blank=True)
    work_finish_year = models.CharField(max_length=255, null=True, blank=True)
    sign_status = models.CharField(max_length=255, null=True, blank=True)
    order_sent_date = models.CharField(max_length=255, null=True, blank=True)
    invoice_payment_plan_date = models.CharField(max_length=255, null=True, blank=True)
    invoice_payment_real_date = models.CharField(max_length=255, null=True, blank=True)
    date_factoring = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
   

    def error(self) -> str:
        months = {
            ' ': 0, 
            'нет плана': 0,
            'закрыт': 100,
            'аннулирован': 100,
            'исключен': 100,
            'заморожен': 100,
            'январь': 1,
            'февраль': 2,
            'март': 3,
            'апрель': 4,
            'май': 5,
            'июнь': 6,
            'июль': 7,
            'август': 8,
            'сентябрь': 9,
            'октябрь': 10,
            'ноябрь': 11,
            'декабрь': 12,
            
        }
        
        current_date = datetime.datetime.now()

# Get the current month and year
        current_month = current_date.month
        current_year = current_date.year
        try: 
            plan_month = months[str(self.plan_month).lower()]
            plan_year = str(self.plan_year).lower()
            plan_month_new = months[str(self.plan_month_new).lower()]
            plan_year_new = str(self.plan_year_new).lower()

            if plan_year == "нет плана": 
                plan_year = 0
            elif plan_year in ('исключен', 'аннулирован', 'закрыт', ' ', 'заморожен'):
                plan_year = 100
            else:
                plan_year = int(plan_year)
            
            if plan_year_new == "нет плана": 
                plan_year_new = 0
            if plan_year_new in ('исключен', 'аннулирован', 'закрыт', ' ', 'заморожен'):
                plan_year_new = 100
            else:
                plan_year_new = int(plan_year_new)
            
            

            if plan_month+1 == current_month and plan_year == current_year:
                plan_month_new = current_month
                plan_year_new = current_year

            
            if plan_year == 0 and plan_month == 0:
                if plan_year_new == 0 and plan_month_new == 0:
                    return "Исправить"
                elif plan_year_new >= current_year:
                    if plan_month_new >= current_month: 
                        return "OK"
                elif plan_month_new < current_month:
                    if plan_year_new > current_year:
                        return "OK"
                    elif plan_year_new < current_year:
                        return "Исправить"
                    elif plan_year_new == current_year:
                        return "Исправить"
                else:
                    return "Исправить"
            
            # if self.error == '':
            #     self.error = 'Исправить'
                
            
            elif plan_year == 100 and plan_month == 100:
                return "OK"

            elif plan_year in ("закрыт","аннулирован","исключен","заморожен"):
                if plan_month in ("закрыт","аннулирован","исключен","заморожен"):
                    return "OK"

            elif plan_year == current_year and plan_month == current_month:
                if plan_month_new == current_month and plan_year_new == current_year:
                    return "ОК"
                elif plan_month_new == current_month + 1 and plan_year_new == current_year:
                    return "Исправить"
            else: 
                return "Исправить"  
            
        except KeyError: 
            return "Исправить"
        

    class Meta:
        ordering = ["created_at"]
        db_table = 'excel_app_mainmodel'
        # Specify the database for this model
        app_label = 'realization_report_KarTel'
        managed = False


@receiver(pre_save, sender=MainModel)
def replace_nat(sender, instance, **kwargs):
    
    if instance.signed_order_date == NaT:
        instance.signed_order_date = None
    if instance.finish_date_plan == NaT:
        instance.finish_date_plan = None
    if instance.date_invoice == NaT:
        instance.date_invoice = None
    if instance.order_sent_date == NaT:
        instance.order_sent_date = None
    if instance.invoice_payment_plan_date == NaT:
        instance.invoice_payment_plan_date = None
    if instance.invoice_payment_real_date == NaT:
        instance.invoice_payment_real_date = None
    if instance.date_factoring == NaT:
        instance.date_factoring = None
    
class PMModel(models.Model):

    def __str__(self) -> str:
        return self.pm or "None"
    
    pm = models.CharField(max_length=255, null=True, blank=True)
    activity_field = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    activity_type = models.CharField(max_length=255, null=True, blank=True)
    project_type = models.CharField(max_length=255, null=True, blank=True)
    customer = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'pm'
        # Specify the database for this model
        app_label = 'pm_kartel'
        managed = False

class PlansModel(models.Model):
    
    def __str__(self) -> str:
        return self.plan_month or "None"

    order_number = models.CharField(max_length=255, null=True, blank=True)
    pm = models.CharField(max_length=255, null=True, blank=True)
    activity_type = models.CharField(max_length=255, null=True, blank=True)
    plan_month = models.CharField(max_length=255, null=True, blank=True)
    plan_year = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'tp'
        app_label = 'plans_T_P'
        managed = False

class ReserveModel(models.Model):
    def __str__(self) -> str:
        return self.order_number or "None"
    
    order_number = models.CharField(max_length=255, null=True, blank=True)
    order_entered_date = models.CharField(max_length=255, null=True, blank=True)
    order_entered_date_month = models.CharField(max_length=255, null=True, blank=True)
    order_entered_date_year = models.CharField(max_length=255, null=True, blank=True)
    podryad_transfer = models.CharField(max_length=255, null=True, blank=True)
    podryad_transfer_month = models.CharField(max_length=255, null=True, blank=True)
    podryad_transfer_year = models.CharField(max_length=255, null=True, blank=True)
    order_number_for_work = models.CharField(max_length=255, null=True, blank=True)
    signed_order_date = models.CharField(max_length=255, null=True, blank=True)
    signed_order_date_month = models.CharField(max_length=255, null=True, blank=True)
    signed_order_date_year = models.CharField(max_length=255, null=True, blank=True)
    work_period_days = models.CharField(max_length=255, null=True, blank=True)
    finish_date_plan = models.CharField(max_length=255, null=True, blank=True)
    left_days_to_finish = models.CharField(max_length=255, null=True, blank=True)
    agreement_status = models.CharField(max_length=255, null=True, blank=True)
    customer = models.CharField(max_length=255, null=True, blank=True)
    provider = models.CharField(max_length=255, null=True, blank=True)
    pm = models.CharField(max_length=255, null=True, blank=True)
    project = models.CharField(max_length=255, null=True, blank=True)
    agreement_attachment = models.CharField(max_length=255, null=True, blank=True)
    partition = models.CharField(max_length=255, null=True, blank=True)
    project_group = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    activity_field = models.CharField(max_length=255, null=True, blank=True)
    activity_type = models.CharField(max_length=255, null=True, blank=True)
    service_range = models.CharField(max_length=255, null=True, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    contract_number = models.CharField(max_length=255, null=True, blank=True)
    contract_sign_date = models.CharField(max_length=255, null=True, blank=True)
    order_sum_vat = models.CharField(max_length=255, null=True, blank=True)
    plan_month = models.CharField(max_length=255, null=True, blank=True)
    plan_year = models.CharField(max_length=255, null=True, blank=True)
    plan_month_new = models.CharField(max_length=255, null=True, blank=True)
    plan_year_new = models.CharField(max_length=255, null=True, blank=True)
    comment_finance = models.CharField(max_length=255, null=True, blank=True)
    comment_pm = models.CharField(max_length=255, null=True, blank=True)
    account_number_avans = models.CharField(max_length=255, null=True, blank=True)
    date_invoice = models.CharField(max_length=255, null=True, blank=True)
    date_avans = models.CharField(max_length=255, null=True, blank=True)
    date_avans_year = models.CharField(max_length=255, null=True, blank=True)
    avans_sum = models.CharField(max_length=255, null=True, blank=True)
    account_number = models.CharField(max_length=255, null=True, blank=True)
    invoice_faktura_number = models.CharField(max_length=255, null=True, blank=True)
    date_invoice_release = models.CharField(max_length=255, null=True, blank=True)
    date_invoice_release_month = models.CharField(max_length=255, null=True, blank=True)
    date_invoice_release_year = models.CharField(max_length=255, null=True, blank=True)
    sum_by_invoice = models.CharField(max_length=255, null=True, blank=True)
    work_type = models.CharField(max_length=255, null=True, blank=True)
    on_who = models.CharField(max_length=255, null=True, blank=True)
    work_status = models.CharField(max_length=255, null=True, blank=True)
    work_finish_month = models.CharField(max_length=255, null=True, blank=True)
    work_finish_year = models.CharField(max_length=255, null=True, blank=True)
    sign_status = models.CharField(max_length=255, null=True, blank=True)
    order_sent_date = models.CharField(max_length=255, null=True, blank=True)
    invoice_payment_plan_date = models.CharField(max_length=255, null=True, blank=True)
    invoice_payment_real_date = models.CharField(max_length=255, null=True, blank=True)
    date_factoring = models.CharField(max_length=255, null=True, blank=True)
    

    class Meta:
        db_table = 'report_kartel_reservemodel'
        app_label = 'reserve_model'

        managed = False