from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from notifications.utils import dispatch_notification
from .models import Homework
from notifications.signals import register_delete_signal

@receiver(post_save, sender=Homework)
def homework_created(sender, instance, created, **kwargs):
    if created:
        message = (
            f"Yeni Ev Tapşırığı: {instance.teacher.get_full_name()} müəllimi "
            f"{instance.classroom.name} sinfi üçün {instance.subject.name} fənnindən yeni tapşırıq əlavə etdi."
        )
        dispatch_notification(
            message=message,
            target_group='PARENT',
            instance=instance
        )

register_delete_signal(Homework)

