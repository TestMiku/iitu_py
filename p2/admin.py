from django.contrib import admin
from .models import Project, WorkType, Document, DocType, Request, WorkRentType, DocumentRent, RejectedDocument, Region

class WorkTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'doc_type')  # Поля, которые будут отображаться в админке

# Регистрируем модель WorkType с соответствующим административным классом
admin.site.register(WorkType, WorkTypeAdmin)

admin.site.register(Project)
admin.site.register(WorkRentType)
admin.site.register(Document)
admin.site.register(DocType)
admin.site.register(Request)
admin.site.register(DocumentRent)
admin.site.register(RejectedDocument)
admin.site.register(Region)
# admin.site.register(Comment)