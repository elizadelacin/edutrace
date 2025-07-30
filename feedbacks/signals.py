from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Feedback
from notifications.utils import dispatch_notification

@receiver(post_save, sender=Feedback)
def feedback_created(sender, instance, created, **kwargs):
    if created:
        dispatch_notification(
            title="Yeni Feedback",
            message=f"{instance.teacher.get_full_name()} sizin övladınız haqqında yeni rəy yazdı.",
            created_by=instance.teacher,
            target_user=instance.student.parent,
        )
