from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'school', 'classroom', 'parent')
    list_filter = ('school', 'classroom')
    search_fields = ('first_name', 'last_name', 'parent__username')
