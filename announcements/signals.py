from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Announcement
from notifications.utils import dispatch_notification

@receiver(post_save, sender=Announcement)
def announcement_created(sender, instance, created, **kwargs):
    if created:
        dispatch_notification(
            title=instance.title,
            message=instance.message,
            created_by=instance.created_by,
            target_group=instance.target_group
        )
