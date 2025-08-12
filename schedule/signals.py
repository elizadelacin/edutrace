from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Schedule
from notifications.signals import dispatch_notification, register_delete_signal
from accounts.models import CustomUser

@receiver(post_save, sender=Schedule)
def schedule_changed(sender, instance, created, **kwargs):
    if created:
        message = f"{instance.classroom.name} sinifinin dərs cədvəlində yeni əlavə edildi."
    else:
        message = f"{instance.classroom.name} sinifinin dərs cədvəlində dəyişiklik edildi."

    # Müəllimlərə bildiriş
    teachers = CustomUser.objects.filter(role='TEACHER')
    for teacher in teachers:
        dispatch_notification(
            user_id=teacher.id,
            message=message,
            content_object=instance
        )

    # Valideynlərə bildiriş
    parents = CustomUser.objects.filter(role='PARENT')
    for parent in parents:
        dispatch_notification(
            user_id=parent.id,
            message=message,
            content_object=instance
        )

register_delete_signal(Schedule)
