from django.contrib import admin
from .models import Schedule


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("classroom", "subject", "teacher", "weekday", "time")
    list_filter = ("weekday", "classroom", "teacher", "subject")
    search_fields = ("classroom__name", "subject__name", "teacher__full_name", "teacher__email")
    ordering = ("weekday", "time")
