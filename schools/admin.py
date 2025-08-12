from django.contrib import admin
from .models import School, ClassRoom, TeachingAssignment

class TeachingAssignmentInline(admin.TabularInline):
    model = TeachingAssignment
    extra = 1
    autocomplete_fields = ['teacher', 'subject']

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone_number', 'email']
    search_fields = ['name', 'phone_number', 'email']

@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'school']
    list_filter = ['school']
    search_fields = ['name', 'school__name']
    inlines = [TeachingAssignmentInline]

@admin.register(TeachingAssignment)
class TeachingAssignmentAdmin(admin.ModelAdmin):
    list_display = ['classroom', 'subject', 'teacher']
    list_filter = ['classroom__school', 'subject']
    search_fields = [
        'classroom__name',
        'teacher__first_name',
        'teacher__last_name',
        'subject__name'
    ]
    autocomplete_fields = ['teacher', 'subject', 'classroom']
