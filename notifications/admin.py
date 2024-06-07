from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'from_whom', 'to_whom', 'is_read', 'created_at')
    search_fields = ('title', 'body', 'from_whom__username', 'to_whom__username')
    list_filter = ('is_read', 'created_at')
    readonly_fields = ('created_at',)


admin.site.register(Notification, NotificationAdmin)

