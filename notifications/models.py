from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Notification(models.Model):
    from_whom = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, default=None, related_name='notifications_sent'
    )
    to_whom = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='notifications_received')
    title = models.CharField(max_length=128)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification from {self.from_whom} to {self.to_whom}"

    @staticmethod
    def create_notification(from_user, to_user, title, body):
        notification = Notification(
            from_whom=from_user,
            to_whom=to_user,
            title=title,
            body=body
        )
        notification.save()
        return notification

    @staticmethod
    def get_latest_notifications(user, limit=5):
        return Notification.objects.filter(to_whom=user).order_by('-created_at')[:limit]
