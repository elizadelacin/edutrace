from .tasks import create_user_notifications

def dispatch_notification(message, target_group=None, target_user_id=None, instance=None):

    model_name = None
    object_id = None

    if instance:
        model_name = instance.__class__.__name__
        object_id = instance.id

    create_user_notifications.delay(
        message,
        target_group,
        target_user_id,
        model_name,
        object_id
    )
