from django.db import models
from django.conf import settings

class Notification(models.Model):
    TARGET_CHOICES = [
        ('ALL', 'All users'),
        ('TEACHERS', 'Teachers only'),
        ('PARENTS', 'Parents only'),
        ('USER', 'Specific user'),
    ]

    title = models.CharField(max_length=255)
    message = models.TextField()
    target_group = models.CharField(max_length=20, choices=TARGET_CHOICES)
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_notifications',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class UserNotification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name='user_notifications'
    )
    is_read = models.BooleanField(default=False)
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'notification')
        ordering = ['-received_at']

    def __str__(self):
        return f"{self.user.email} - {self.notification.title}"
