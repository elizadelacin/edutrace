from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Schedule
from notifications.utils import dispatch_notification
from notifications.signals import register_delete_signal

@receiver(post_save, sender=Schedule)
def schedule_changed(sender, instance, created, **kwargs):
    if created:
        message = f"{instance.classroom.name} sinifinin dərs cədvəlində yeni əlavə edildi."
    else:
        message = f"{instance.classroom.name} sinifinin dərs cədvəlində dəyişiklik edildi."

    dispatch_notification(
        message=message,
        target_group='TEACHER',
        instance=instance,
    )
    dispatch_notification(
        message=message,
        target_group='PARENT',
        instance=instance,
    )

register_delete_signal(Schedule)

