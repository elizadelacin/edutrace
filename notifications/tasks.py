from celery import shared_task
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from .models import UserNotification

User = get_user_model()

@shared_task
def create_user_notifications(message, target_group=None, target_user_id=None, model_name=None, object_id=None):
    content_type = None
    if model_name and object_id:
        try:
            content_type = ContentType.objects.get(model=model_name.lower())
        except ContentType.DoesNotExist:
            content_type = None

    if target_user_id:
        try:
            user = User.objects.get(id=target_user_id)
            UserNotification.objects.create(
                user=user,
                message=message,
                content_type=content_type,
                object_id=object_id
            )
        except User.DoesNotExist:
            pass
    elif target_group:
        users = User.objects.filter(role=target_group)
        notifications = [
            UserNotification(
                user=user,
                message=message,
                content_type=content_type,
                object_id=object_id
            )
            for user in users
        ]
        UserNotification.objects.bulk_create(notifications)
