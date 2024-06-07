from django.contrib import admin
from .models import Supplier,Adem_19_20, Merged_model,ESF_A77

# Register your models here.
class MergedModelAdmin(admin.ModelAdmin):
    list_display = ('date', 'documentno', 'nscheta', 'datascheta', 'too', 'postavshik', 'bin', 'notpayamt1ckzt', 'gruppa_proekrov', 'docdate', 'matched')
    list_filter = ('matched',)
    
admin.site.register(Supplier)
admin.site.register(Adem_19_20)
admin.site.register(Merged_model, MergedModelAdmin)
admin.site.register(ESF_A77)


