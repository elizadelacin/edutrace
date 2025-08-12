from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from accounts.models import CustomUser
from notifications.models import UserNotification

User = get_user_model()

def send_realtime_notification(user_id, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"user_{user_id}",
        {
            "type": "send_notification",
            "content": {
                "message": message
            }
        }
    )

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

def dispatch_notification(user_id, message, content_object=None):
    user = CustomUser.objects.get(id=user_id)
    content_type = None
    object_id = None

    if content_object is not None:
        content_type = ContentType.objects.get_for_model(content_object.__class__)
        object_id = content_object.pk

    notification = UserNotification.objects.create(
        user=user,
        message=message,
        content_type=content_type,
        object_id=object_id
    )

    send_realtime_notification(user.id, message)

    return notification