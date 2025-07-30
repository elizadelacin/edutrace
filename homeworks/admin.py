from django.contrib import admin
from .models import Homework

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'classroom', 'subject', 'teacher', 'due_date']
    list_filter = ['classroom', 'subject', 'teacher']
