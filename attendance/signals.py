from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Attendance
from notifications.utils import dispatch_notification
from notifications.signals import register_delete_signal

@receiver(post_save, sender=Attendance)
def attendance_marked(sender, instance, created, **kwargs):
    if instance.student.parent and instance.subject:
        status = 'qatıldı' if instance.status == 'PRESENT' else 'qatılmadı'
        subject_name = instance.subject.name
        message = (
            f"{instance.student.get_full_name()} {subject_name} dərsinə {status}."
        )
        dispatch_notification(
            message=message,
            target_user_id=instance.student.parent.id,
            instance=instance
        )

register_delete_signal(Attendance)
