from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Notification, UserNotification

User = get_user_model()


@shared_task
def create_user_notifications(notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
    except Notification.DoesNotExist:
        return

    if notification.target_group == 'ALL':
        users = User.objects.all()
    elif notification.target_group == 'TEACHERS':
        users = User.objects.filter(role='TEACHER')
    elif notification.target_group == 'PARENTS':
        users = User.objects.filter(role='PARENT')
    elif notification.target_group == 'USER' and notification.target_user:
        users = [notification.target_user]
    else:
        users = []

    user_notifications = []
    for user in users:
        user_notifications.append(UserNotification(user=user, notification=notification))

    UserNotification.objects.bulk_create(user_notifications)
