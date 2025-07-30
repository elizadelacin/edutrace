from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Schedule
from students.models import Student
from notifications.utils import dispatch_notification

@receiver(post_save, sender=Schedule)
def schedule_changed(sender, instance, created, **kwargs):
    # Planlama dəyişdikdə həm müəllimlər, həm valideynlər üçün bildiriş göndər
    dispatch_notification(
        title="Dərs Cədvəlində Dəyişiklik",
        message=f"{instance.classroom.name} sinifinin dərs cədvəlində dəyişiklik edildi.",
        created_by=instance.created_by,
        target_group='TEACHERS',
    )
    dispatch_notification(
        title="Dərs Cədvəlində Dəyişiklik",
        message=f"{instance.classroom.name} sinifinin dərs cədvəlində dəyişiklik edildi.",
        created_by=instance.created_by,
        target_group='PARENTS',
    )
