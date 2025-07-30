from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Attendance
from notifications.utils import dispatch_notification

@receiver(post_save, sender=Attendance)
def attendance_marked(sender, instance, created, **kwargs):
    if created:
        dispatch_notification(
            title="Dərs İştirakı Qeyd Edildi",
            message=f"{instance.student.get_full_name()} dərsə { 'qatıldı' if instance.is_present else 'qatılmadı' }.",
            created_by=instance.teacher,
            target_user=instance.student.parent,
        )
