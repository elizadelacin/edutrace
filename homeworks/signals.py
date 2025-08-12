from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from notifications.signals import dispatch_notification, register_delete_signal
from .models import Homework
from accounts.models import CustomUser

@receiver(post_save, sender=Homework)
def homework_created(sender, instance, created, **kwargs):
    if created:
        message = (
            f"Yeni Ev Tapşırığı: {instance.teacher.get_full_name()} müəllimi "
            f"{instance.classroom.name} sinfi üçün {instance.subject.name} fənnindən yeni tapşırıq əlavə etdi."
        )
        # Bütün valideyn istifadəçilərini tapırıq
        parents = CustomUser.objects.filter(role='PARENT')

        for parent in parents:
            dispatch_notification(
                user_id=parent.id,
                message=message,
                content_object=instance
            )

register_delete_signal(Homework)
