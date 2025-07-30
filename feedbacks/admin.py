from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher', 'parent', 'student', 'created_at')
    search_fields = ('teacher__username', 'parent__username', 'student__full_name', 'message')
    list_filter = ('created_at',)
