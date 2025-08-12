from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Announcement
from notifications.signals import dispatch_notification, register_delete_signal
from accounts.models import CustomUser

@receiver(post_save, sender=Announcement)
def send_announcement_notification(sender, instance, created, **kwargs):
    if created:
        if instance.target_group == 'ALL':
            users = CustomUser.objects.all()
        elif instance.target_group == 'TEACHERS':
            users = CustomUser.objects.filter(role='TEACHER')
        elif instance.target_group == 'PARENTS':
            users = CustomUser.objects.filter(role='PARENT')
        else:
            users = CustomUser.objects.none()

        for user in users:
            dispatch_notification(
                user_id=user.id,
                message=f"Yeni elan: {instance.title}",
                content_object=instance
            )

register_delete_signal(Announcement)
