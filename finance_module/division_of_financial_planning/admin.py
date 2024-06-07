from django.contrib import admin

from . import models


@admin.register(models.Table)
class TableAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(models.Row)
class RowAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(models.Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ["id", "row", "field", "type", "date", "value"]
    search_fields = ["field"]
