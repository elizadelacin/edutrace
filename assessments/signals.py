from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DailyAssessment, ExamAssessment
from students.models import Student
from notifications.utils import dispatch_notification

@receiver(post_save, sender=DailyAssessment)
def daily_assessment_created(sender, instance, created, **kwargs):
    if created:
        dispatch_notification(
            title="Yeni Günlük Qiymətləndirmə",
            message=f"{instance.teacher.get_full_name()} müəllimi tərəfindən {instance.subject.name} fənnindən yeni qiymətləndirmə əlavə olundu.",
            created_by=instance.teacher,
            target_user=instance.student.parent,
        )

@receiver(post_save, sender=ExamAssessment)
def exam_assessment_created(sender, instance, created, **kwargs):
    if created and instance.type != 'YI':
        dispatch_notification(
            title="Yeni İmtahan Qiymətləndirməsi",
            message=f"{instance.teacher.get_full_name()} müəllimi tərəfindən {instance.subject.name} fənnindən imtahan qiymətləndirməsi əlavə olundu.",
            created_by=instance.teacher,
            target_user=instance.student.parent,
        )
