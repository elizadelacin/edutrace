from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DailyAssessment, ExamAssessment
from notifications.signals import dispatch_notification, register_delete_signal

@receiver(post_save, sender=DailyAssessment)
def daily_assessment_created(sender, instance, created, **kwargs):
    if created and instance.student.parent:
        parent_user_id = instance.student.parent.id
        message = (
            f"Yeni Günlük Qiymətləndirmə: {instance.teacher.get_full_name()} müəllimi "
            f"{instance.subject.name} fənnindən sizin övladınıza qiymət əlavə etdi."
        )
        dispatch_notification(
            user_id=parent_user_id,
            message=message,
            content_object=instance
        )

@receiver(post_save, sender=ExamAssessment)
def exam_assessment_created(sender, instance, created, **kwargs):
    if created and instance.student.parent:
        parent_user_id = instance.student.parent.id  # Burada da .user silindi
        message = (
            f"Yeni İmtahan Qiymətləndirməsi: {instance.teacher.get_full_name()} müəllimi "
            f"{instance.subject.name} fənnindən sizin övladınıza imtahan qiyməti əlavə etdi."
        )
        dispatch_notification(
            user_id=parent_user_id,
            message=message,
            content_object=instance
        )

register_delete_signal(DailyAssessment)
register_delete_signal(ExamAssessment)
