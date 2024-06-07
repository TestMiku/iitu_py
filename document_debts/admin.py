from django.contrib import admin
from .models import DebtChangesHistory, DebtDocument, DebtImportError, DebtSupplier, DebtPermanentFilter, DebtStatus
# Register your models here.
admin.site.register(DebtSupplier)
admin.site.register(DebtStatus)
admin.site.register(DebtImportError)
admin.site.register(DebtChangesHistory)
admin.site.register(DebtPermanentFilter)

class DebtDocumentAdmin(admin.ModelAdmin):
    search_fields = ['documentno']  
admin.site.register(DebtDocument, DebtDocumentAdmin)

