from django.contrib import admin
from .models import DailyAssessment, ExamAssessment

@admin.register(DailyAssessment)
class DailyAssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'subject', 'classroom', 'teacher', 'score', 'date')
    list_filter = ('teacher', 'subject', 'classroom')
    search_fields = ('student__first_name', 'student__last_name', 'subject__name')

@admin.register(ExamAssessment)
class ExamAssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'subject', 'classroom', 'teacher', 'score', 'exam_type', 'date')
    list_filter = ('exam_type', 'teacher', 'subject', 'classroom')
    search_fields = ('student__first_name', 'student__last_name', 'subject__name')
