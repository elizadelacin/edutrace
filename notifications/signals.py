from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from .tasks import create_user_notifications

@receiver(post_save, sender=Notification)
def notification_post_save(sender, instance, created, **kwargs):
    if created:
        create_user_notifications.delay(instance.id)
