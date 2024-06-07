from django.contrib import admin
from calculator.models import *


class COrderAdmin(admin.ModelAdmin):
    search_fields = ["id", "number"]


class COrderPositionAdmin(admin.ModelAdmin):
    search_fields = ["id", "position_name", "order__number"]
    list_display = [
        "order_number",
        "position_name",
        "article",
        "quantity",
        "default_sum",
    ]

    def order_number(self, obj):
        return obj.order.number

    def article(self, obj: COrderPosition) -> str | None:
        try:
            return COrderPositionPrice.objects.get(customer=obj.position_name, customer_name=obj.order.customer_name).contractor
        except COrderPositionPrice.DoesNotExist:
            return None


    def default_sum(self, obj):
        return obj.get_default_sum

    default_sum.short_description = "Сумма позиции"
    article.short_description = "Пункт ТЦП с подрядчиком"
    order_number.short_description = "Номер заказа"
    


class COrderPositionPriceAdmin(admin.ModelAdmin):
    search_fields = ["id", "find_key", "contractor"]


admin.site.register(COrder, COrderAdmin)
admin.site.register(COrderPosition, COrderPositionAdmin)
admin.site.register(COrderPositionPrice, COrderPositionPriceAdmin)
