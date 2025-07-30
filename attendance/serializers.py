from rest_framework import serializers
from .models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'student_name', 'subject', 'classroom', 'teacher', 'date', 'status']
        read_only_fields = ['id', 'teacher', 'date', 'student_name']
