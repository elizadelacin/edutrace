from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'target_group', 'created_by', 'created_at']
    list_filter = ['target_group', 'created_at']
    search_fields = ['title', 'message']
