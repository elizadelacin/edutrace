from django.contrib import admin
from .models import School, ClassRoom

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'created_at')
    search_fields = ('name', 'email')

@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'school', 'created_at')
    list_filter = ('school',)
    filter_horizontal = ('teachers',)
