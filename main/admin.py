# Register your models here.
from django.contrib import admin

from main.models import AvhRole, AvhUser, Chapter, ChapterGroup


@admin.register(AvhUser)
class AvhUserAdmin(admin.ModelAdmin):
    search_fields = ["id", "email", "first_name", "last_name"]
    pass  # Просто регистрируем модель без дополнительных настроек


admin.site.register(ChapterGroup)
admin.site.register(Chapter)
admin.site.register(AvhRole)
