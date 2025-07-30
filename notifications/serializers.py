from rest_framework import serializers
from .models import Notification, UserNotification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at']

class UserNotificationSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer(read_only=True)

    class Meta:
        model = UserNotification
        fields = ['id', 'notification', 'is_read', 'received_at']
