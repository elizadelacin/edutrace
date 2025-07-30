from .models import Notification

def dispatch_notification(title, message, created_by, target_group=None, target_user=None):
    notification = Notification.objects.create(
        title=title,
        message=message,
        created_by=created_by,
        target_group=target_group or ('USER' if target_user else 'ALL'),
        target_user=target_user if target_user else None,
    )
    return notification
