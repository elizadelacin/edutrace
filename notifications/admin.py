from django.contrib import admin
from .models import Notification, UserNotification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'target_group', 'created_by', 'created_at']
    list_filter = ['target_group', 'created_at']
    search_fields = ['title', 'message', 'created_by__email']

@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification', 'is_read', 'received_at']
    list_filter = ['is_read', 'received_at']
    search_fields = ['user__email', 'notification__title']
