from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Feedback
from notifications.utils import dispatch_notification
from notifications.signals import register_delete_signal

@receiver(post_save, sender=Feedback)
def feedback_created(sender, instance, created, **kwargs):
    if created and instance.student.parent:
        message = (
            f"{instance.subject.name} fənnindən sizin övladınız haqqında yeni rəy yazıldı."
        )
        dispatch_notification(
            message=message,
            target_user_id=instance.student.parent.id,
            instance=instance
        )

register_delete_signal(Feedback)
