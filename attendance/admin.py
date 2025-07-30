from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'classroom', 'teacher', 'date', 'status']
    list_filter = ['date', 'classroom', 'subject', 'status']
