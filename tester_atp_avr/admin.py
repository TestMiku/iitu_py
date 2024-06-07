from django.contrib import admin

from . import models

# Register your models here.


class TCPModelAdmin(admin.ModelAdmin):
    list_display = ["number", "name", "price", "measuring_unit"]
    search_fields = ["name", "price"]


admin.site.register(models.TCP, TCPModelAdmin)
admin.site.register(models.TCPCategory)
admin.site.register(models.TCPFile)
admin.site.register(models.WorkType)
admin.site.register(models.ContratcNumberAndDate)
