from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Homework
from students.models import Student
from notifications.utils import dispatch_notification

@receiver(post_save, sender=Homework)
def homework_created(sender, instance, created, **kwargs):
    if created:
        dispatch_notification(
            title="Yeni Ev Tapşırığı",
            message=f"{instance.teacher.get_full_name()} müəllimi yeni ev tapşırığı əlavə etdi.",
            created_by=instance.teacher,
            target_group='PARENTS',
        )
