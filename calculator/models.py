from django.db import models
from django.utils.translation import gettext_lazy as _

from main.models import AvhObject


class COrder(AvhObject):
    number = models.CharField(_("Номер заказа"), max_length=50, unique=True)
    region = models.CharField(_("Регион"), max_length=1500, null=True)
    comments = models.CharField(_("Комментарии"), max_length=1500)
    customer_name = models.CharField(
        _("Заказчик"), max_length=200, default="КаР-Тел, ТОО", blank=True, null=True
    )
    buyigrandtotal = models.FloatField(_("На какую сумму заведены ДО"), default=0)
    money_wasted = models.FloatField(_("Фактически потрачено на заказ"), default=0)
    
    def __str__(self):
        return self.number

class HeaderPosition(AvhObject):
    # order = models.ForeignKey("calculator.COrder", verbose_name=_("Пункт заказа"), related_name="header_positions", on_delete=models.CASCADE)
    order_number = models.CharField(default='', null=True, max_length=1500)
    idocumentno = models.CharField(default='', null=True, max_length=1500)
    iprovider = models.CharField(default='', null=True, max_length=1500)
    iconfirmer = models.CharField(default='', null=True, max_length=1500)
    taxincluded = models.CharField(default='', null=True, max_length=1500)
    idescription = models.CharField(default='', null=True, max_length=1500)
    odescription = models.CharField(default='', null=True, max_length=1500)
    odateordered = models.CharField(default='', null=True, max_length=1500)
    category = models.CharField(default='', null=True, max_length=1500)
    iagreement = models.CharField(default='', null=True, max_length=1500)
    consumer = models.CharField(default='', null=True, max_length=1500)
    refundamtonorder = models.FloatField(default=0, null=True)
    summagreement = models.FloatField(default=0, null=True)
    buyigrandtotal = models.FloatField(default=0, null=True)
    totallines_7_15 = models.FloatField(default=0, null=True)
    region = models.CharField(default='', null=True, max_length=1500)
    project_manager = models.CharField(default='', null=True, max_length=1500)
    productname = models.CharField(default='', null=True, max_length=1500)


class Data7112(AvhObject):
    order_number = models.CharField(default='', null=True, max_length=1500)
    idocumentno = models.CharField(default='', null=True, max_length=1500)
    iprovider = models.CharField(default='', null=True, max_length=1500)
    iconfirmer = models.CharField(default='', null=True, max_length=1500)
    taxincluded = models.CharField(default='', null=True, max_length=1500)
    idescription = models.CharField(default='', null=True, max_length=1500)
    odescription = models.CharField(default='', null=True, max_length=1500)
    odateordered = models.CharField(default='', null=True, max_length=1500)
    category = models.CharField(default='', null=True, max_length=1500)
    iagreement = models.CharField(default='', null=True, max_length=1500)
    consumer = models.CharField(default='', null=True, max_length=1500)
    refundamtonorder = models.FloatField(default=0, null=True)
    summagreement = models.FloatField(default=0, null=True)
    buyigrandtotal = models.FloatField(default=0, null=True)
    totallines_7_15 = models.FloatField(default=0, null=True)
    region = models.CharField(default='', null=True, max_length=1500)
    project_manager = models.CharField(default='', null=True, max_length=1500)
    productname = models.CharField(default='', null=True, max_length=1500)


class COrderPosition(AvhObject):
    order = models.ForeignKey( "calculator.COrder", verbose_name=_("Пункт заказа"), related_name="positions", on_delete=models.CASCADE, )
    quantity = models.FloatField(_("Количество"), default=0)
    comments = models.CharField(_("Комментарии"), max_length=1500)
    position_name = models.CharField(_("Наименование работ с заказчиком"), max_length=1500)
    project_group = models.CharField(
        _("Группа проектов"), max_length=500, default="", blank=True, null=True
    )
    used_count = models.IntegerField(_("Использовано"), default=0, null=True, blank=True)
    used_summ = models.FloatField(_("Сумма использованых"), default=0)
    used_quantity = models.FloatField(_("Количество использованых"), default=0)
    
    @property
    def position(self):
        position = COrderPositionPrice.objects.filter(
            customer=self.position_name, customer_name=self.order.customer_name
        )
        if position:
            return position.last()
        return None

    @property
    def get_max_count(self):
        return f"{self.quantity}".replace(",", ".")

    @property
    def get_max_price(self):
        return f"{round((self.position.price or 0)*0.77, 2)}".replace( #self.position.maximum_price
            ",", "."
        )

    @property
    def get_default_sum(self):
        if self.position:
            return f"{(self.position.price or 0)*0.77 * (self.quantity - self.used_quantity)}".replace( #self.position.maximum_price
                ",", "."
            )
        else: 
            return "0.00"

    def __str__(self):
        return f"{self.order.number} - {self.position_name}"


class COrderPositionPrice(AvhObject):
    find_key = models.CharField(_("Ключ поиска в Адеме"), max_length=50)
    customer_name = models.CharField(
        _("Заказчик"), max_length=100, default=None, blank=True, null=True
    )
    contractor = models.CharField(_("Пункт ТЦП с подрядчиком"), max_length=1500)
    customer = models.CharField(_("Пункт ТЦП Заказчика"), max_length=1500)
    maximum_price = models.IntegerField(
        _("Максимально допустимый процент цены"), default=80
    )
    minimum_price = models.IntegerField(
        _("Минимально допустимый процент цены"), default=80
    )
    default_price = models.IntegerField(_("Процент цены по умолчанию"), default=80)
    price = models.FloatField(_("Цена"), blank=True, null=True)
    price_first = models.FloatField(_("Цена Южные регионы"), blank=True, null=True)
    price_second = models.FloatField(
        _("Цена СевероВосточные регионы"), blank=True, null=True
    )
    price_third = models.FloatField(_("Цена Западные регионы"), blank=True, null=True)
    notes = models.CharField(_("Заметки"), max_length=500, default="")
   
    def get_default_price(self):
        return (self.price or 0) * 0.77

    def __str__(self):
        return self.customer


class Data2122(models.Model):
    order_number = models.CharField(max_length=255, null=True)
    margin = models.FloatField(default=0, null=True)
    activity_field = models.CharField(max_length=255, null=True)
    activity_kind = models.CharField(max_length=255, null=True)
