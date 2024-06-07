from django.db import models
from main.models import AvhObject


class Nomenclature(AvhObject):
    """ Номенклатура. """

    key_product = models.CharField(max_length=255, verbose_name='Ключ продукта')
    name = models.CharField(max_length=255, verbose_name='Название продукта')
    unit = models.CharField(max_length=255, verbose_name='Единица измерения')
    expense_item = models.CharField(max_length=255, verbose_name='Статья расходов')

    def __str__(self):
        return f'{self.key_product} - {self.name}'

    class Meta:
        verbose_name = 'nomenclature'
        verbose_name_plural = 'nomenclatures'
        db_table = 'nomenclature'


class NomenclatureOrder(AvhObject):
    """ Номенклатурный заказ. """

    nomenclature = models.ForeignKey(Nomenclature, on_delete=models.CASCADE, verbose_name='Номенклатура')
    key_search = models.CharField(max_length=255, verbose_name='Ключ поиска')
    quantity = models.IntegerField(verbose_name='Количество (в счете)')
    tax = models.CharField(max_length=255, verbose_name='Налог')
    invoice_line = models.CharField(max_length=255, verbose_name='Строка счета')
    quantity_entered = models.IntegerField(verbose_name='Количество введененное')
    order = models.CharField(max_length=255, verbose_name='Заказ')
    order_specification = models.CharField(max_length=255, verbose_name='Спецификация заказа')
    total_sum = models.IntegerField(verbose_name='Итоговая сумма')

    def __str__(self):
        return f'{self.nomenclature} - {self.key_search}'

    class Meta:
        verbose_name = 'nomenclature_order'
        verbose_name_plural = 'nomenclature_orders'
        db_table = 'nomenclature_order'
