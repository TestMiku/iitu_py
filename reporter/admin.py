from django.contrib import admin

from . import models

class ReportAdmin(admin.ModelAdmin):
    list_display = ['text', 'process', 'responsible', 'created_at']
    search_fields = ['process', 'responsible']

admin.site.register(models.Report, ReportAdmin)
