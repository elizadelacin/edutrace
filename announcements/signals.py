from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Announcement
from notifications.utils import dispatch_notification
from notifications.signals import register_delete_signal

@receiver(post_save, sender=Announcement)
def send_announcement_notification(sender, instance, created, **kwargs):
    if created:
        dispatch_notification(
            message=f"Yeni elan: {instance.title}",
            target_group=instance.target_group,
            instance=instance
        )

register_delete_signal(Announcement)

