from django.contrib import admin
from .models import Assessment, AssessmentResult

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'teacher', 'classroom', 'date')
    list_filter = ('subject', 'date')

@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
    list_display = ('assessment', 'student', 'score')
    list_filter = ('assessment',)
