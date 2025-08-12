from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from notifications.models import UserNotification

def delete_related_notifications(instance):

    content_type = ContentType.objects.get_for_model(instance.__class__)
    UserNotification.objects.filter(
        content_type=content_type,
        object_id=instance.id
    ).delete()

def register_delete_signal(model):
    @receiver(post_delete, sender=model)
    def _delete_notifications(sender, instance, **kwargs):
        delete_related_notifications(instance)
