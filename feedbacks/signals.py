from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Feedback
from notifications.signals import dispatch_notification, register_delete_signal

@receiver(post_save, sender=Feedback)
def feedback_created(sender, instance, created, **kwargs):
    if created and instance.student.parent:
        parent_user_id = instance.student.parent.id  # Burada .user çıxarıldı
        message = (
            f"{instance.subject.name} fənnindən sizin övladınız haqqında yeni rəy yazıldı."
        )
        dispatch_notification(
            user_id=parent_user_id,
            message=message,
            content_object=instance
        )

register_delete_signal(Feedback)
